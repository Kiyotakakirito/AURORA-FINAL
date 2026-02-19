import httpx
import json
import re
from typing import Dict, Any, Optional, List
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

class OllamaService:
    """Service for interacting with Ollama API"""
    
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
        self.timeout = 300  # 5 minutes timeout for evaluation tasks
    
    async def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Make a request to Ollama API"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/{endpoint}",
                    json=data
                )
                response.raise_for_status()
                return response.json()
        except httpx.TimeoutException:
            logger.error(f"Ollama request timeout for {endpoint}")
            return None
        except httpx.HTTPStatusError as e:
            logger.error(f"Ollama HTTP error: {e}")
            return None
        except Exception as e:
            logger.error(f"Ollama connection error: {e}")
            return None
    
    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Optional[str]:
        """Generate a response from Ollama model"""
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        if system_prompt:
            data["system"] = system_prompt
        
        response = await self._make_request("api/generate", data)
        
        if response and "response" in response:
            return response["response"]
        return None
    
    async def generate_json_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        schema: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Generate a structured JSON response from Ollama model"""
        print(f"\n[OLLAMA] generate_json_response called")
        print(f"[OLLAMA] Prompt length: {len(prompt)} chars")
        
        if schema:
            prompt += f"\n\nPlease respond with valid JSON that matches this schema: {json.dumps(schema)}"
        
        # Add explicit instruction for JSON-only response
        prompt += "\n\nIMPORTANT: Return ONLY the JSON array/object without any markdown formatting, explanations, or additional text. Just the raw JSON."
        
        response_text = await self.generate_response(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.1,  # Very low temperature for structured output
            max_tokens=3000
        )
        
        print(f"[OLLAMA] Raw response text length: {len(response_text) if response_text else 0}")
        print(f"[OLLAMA] Raw response preview: {response_text[:200] if response_text else 'None'}")
        
        if not response_text:
            print("[OLLAMA] ERROR: No response text received")
            return None
        
        try:
            # Try multiple extraction methods
            json_text = None
            
            # Method 1: Extract from markdown code blocks
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
            
            # Method 2: Find JSON array or object boundaries
            if not json_text:
                # Look for array
                arr_start = response_text.find("[")
                arr_end = response_text.rfind("]")
                # Look for object
                obj_start = response_text.find("{")
                obj_end = response_text.rfind("}")
                
                # Use whichever has valid structure
                if arr_start != -1 and arr_end != -1 and arr_end > arr_start:
                    json_text = response_text[arr_start:arr_end+1].strip()
                elif obj_start != -1 and obj_end != -1 and obj_end > obj_start:
                    json_text = response_text[obj_start:obj_end+1].strip()
            
            # Method 3: Clean up common issues and try parsing entire text
            if not json_text:
                json_text = response_text.strip()
                # Remove markdown formatting
                json_text = re.sub(r'```[\w]*\n?', '', json_text)
                json_text = re.sub(r'```', '', json_text)
                # Remove explanatory text before/after JSON
                json_text = re.sub(r'^[^{\[]*', '', json_text)
                json_text = re.sub(r'[^}\]]*$', '', json_text)
            
            if json_text:
                result = json.loads(json_text)
                print(f"[OLLAMA] Successfully parsed JSON with keys: {list(result.keys()) if isinstance(result, dict) else 'N/A'}")
                return result
            
            print("[OLLAMA] ERROR: No valid JSON text found after extraction")
            return None
            
        except json.JSONDecodeError as e:
            print(f"[OLLAMA] ERROR: JSON parse failed: {e}")
            print(f"[OLLAMA] Raw text that failed: {response_text[:500]}")
            return None
    
    async def list_models(self) -> List[str]:
        """List available models in Ollama"""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                response.raise_for_status()
                data = response.json()
                
                if "models" in data:
                    return [model["name"] for model in data["models"]]
                return []
        except Exception as e:
            logger.error(f"Failed to list Ollama models: {e}")
            return []
    
    async def check_connection(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama connection check failed: {e}")
            return False
    
    async def pull_model(self, model_name: str) -> bool:
        """Pull a model from Ollama"""
        try:
            async with httpx.AsyncClient(timeout=600) as client:  # 10 minutes timeout
                response = await client.post(
                    f"{self.base_url}/api/pull",
                    json={"name": model_name}
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to pull model {model_name}: {e}")
            return False

# Global instance
ollama_service = OllamaService()
