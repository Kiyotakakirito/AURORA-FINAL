import httpx
import json
import re
from typing import Dict, Any, Optional, List
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)


class OllamaService:
    """Service for interacting with Ollama API (local or Ollama Cloud)."""

    def __init__(self):
        self.base_url = settings.ollama_base_url.rstrip("/")
        self.model = settings.ollama_model
        # Short connect timeout so unreachable hosts fail fast (→ fallback).
        # Read timeout is generous since generation can be slow.
        self.timeout = httpx.Timeout(connect=5.0, read=120.0, write=30.0, pool=5.0)
        self.api_key = settings.ollama_api_key  # None → local Ollama (no auth)

    # ── helpers ────────────────────────────────────────────────────────────

    def _auth_headers(self) -> dict:
        """Return Authorization header when an API key is configured."""
        if self.api_key:
            return {"Authorization": f"Bearer {self.api_key}"}
        return {}

    def _is_cloud(self) -> bool:
        """True when pointing at Ollama Cloud (ollama.com), not localhost."""
        return "ollama.com" in self.base_url

    # ── availability check ─────────────────────────────────────────────────

    async def check_available(self) -> bool:
        """Return True if Ollama is reachable. Uses a 3s connect timeout so
        the caller knows immediately when Ollama is down."""
        try:
            fast_timeout = httpx.Timeout(connect=3.0, read=5.0, write=5.0, pool=3.0)
            url = f"{self.base_url}/api/tags"
            async with httpx.AsyncClient(timeout=fast_timeout) as client:
                r = await client.get(url, headers=self._auth_headers())
                return r.status_code < 500
        except Exception as e:
            logger.warning(f"Ollama not available: {e}")
            return False

    # ── core request ───────────────────────────────────────────────────────

    async def _chat_request(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> Optional[str]:
        """
        POST to /chat using the Ollama messages format.
        Works for both local Ollama and Ollama Cloud.
        """
        data = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }

        # Cloud uses /chat; local uses /api/chat
        if self._is_cloud():
            url = f"{self.base_url}/chat"
        else:
            url = f"{self.base_url}/api/chat"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    url, json=data, headers=self._auth_headers()
                )
                response.raise_for_status()
                result = response.json()

                # Extract content from message
                msg = result.get("message", {})
                return msg.get("content") or result.get("response")
        except httpx.TimeoutException:
            logger.error(f"Ollama request timeout: {url}")
        except httpx.HTTPStatusError as e:
            logger.error(f"Ollama HTTP error {e.response.status_code}: {e.response.text[:300]}")
        except Exception as e:
            logger.error(f"Ollama connection error: {e}")
        return None

    # ── public API (kept identical to old interface) ───────────────────────

    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> Optional[str]:
        """Generate a text response from the Ollama model."""
        messages: List[Dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        return await self._chat_request(
            messages, temperature=temperature, max_tokens=max_tokens
        )

    async def generate_json_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        schema: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        """Generate a structured JSON response from the Ollama model."""
        print(f"\n[OLLAMA] generate_json_response called")
        print(f"[OLLAMA] Prompt length: {len(prompt)} chars")

        if schema:
            prompt += f"\n\nPlease respond with valid JSON that matches this schema: {json.dumps(schema)}"

        prompt += (
            "\n\nIMPORTANT: Return ONLY the JSON array/object without any markdown "
            "formatting, explanations, or additional text. Just the raw JSON."
        )

        response_text = await self.generate_response(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.1,
            max_tokens=3000,
        )

        print(f"[OLLAMA] Raw response text length: {len(response_text) if response_text else 0}")
        print(f"[OLLAMA] Raw response preview: {response_text[:200] if response_text else 'None'}")

        if not response_text:
            print("[OLLAMA] ERROR: No response text received")
            return None

        try:
            json_text = None

            # Method 1: markdown code blocks
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                if json_end != -1:
                    json_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                if json_end != -1:
                    json_text = response_text[json_start:json_end].strip()

            # Method 2: find JSON array / object boundaries
            if not json_text:
                arr_start = response_text.find("[")
                arr_end = response_text.rfind("]")
                obj_start = response_text.find("{")
                obj_end = response_text.rfind("}")

                if arr_start != -1 and arr_end != -1 and arr_end > arr_start:
                    json_text = response_text[arr_start : arr_end + 1].strip()
                elif obj_start != -1 and obj_end != -1 and obj_end > obj_start:
                    json_text = response_text[obj_start : obj_end + 1].strip()

            # Method 3: clean up markdown formatting
            if not json_text:
                json_text = response_text.strip()
                json_text = re.sub(r"```[\w]*\n?", "", json_text)
                json_text = re.sub(r"```", "", json_text)
                json_text = re.sub(r"^[^{\[]*", "", json_text)
                json_text = re.sub(r"[^}\]]*$", "", json_text)

            if json_text:
                result = json.loads(json_text)
                print(
                    f"[OLLAMA] Successfully parsed JSON with keys: "
                    f"{list(result.keys()) if isinstance(result, dict) else 'N/A'}"
                )
                return result

            print("[OLLAMA] ERROR: No valid JSON text found after extraction")
            return None

        except json.JSONDecodeError as e:
            print(f"[OLLAMA] ERROR: JSON parse failed: {e}")
            print(f"[OLLAMA] Raw text that failed: {response_text[:500]}")
            return None

    async def list_models(self) -> List[str]:
        """List available models."""
        if self._is_cloud():
            url = f"{self.base_url}/tags"
        else:
            url = f"{self.base_url}/api/tags"

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(url, headers=self._auth_headers())
                response.raise_for_status()
                data = response.json()
                if "models" in data:
                    return [model["name"] for model in data["models"]]
                return []
        except Exception as e:
            logger.error(f"Failed to list Ollama models: {e}")
            return []

    async def check_connection(self) -> bool:
        """Check if Ollama is running and accessible."""
        if self._is_cloud():
            url = f"{self.base_url}/tags"
        else:
            url = f"{self.base_url}/api/tags"

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url, headers=self._auth_headers())
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama connection check failed: {e}")
            return False

    async def pull_model(self, model_name: str) -> bool:
        """Pull a model (local Ollama only)."""
        if self._is_cloud():
            logger.info("pull_model is not supported for Ollama Cloud; skipping.")
            return True  # no-op on cloud

        try:
            async with httpx.AsyncClient(timeout=600) as client:
                response = await client.post(
                    f"{self.base_url}/api/pull",
                    json={"name": model_name},
                    headers=self._auth_headers(),
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to pull model {model_name}: {e}")
            return False


# Global instance
ollama_service = OllamaService()
