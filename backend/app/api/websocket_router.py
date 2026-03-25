"""
WebSocket router for real-time evaluation progress streaming.
"""
import asyncio
import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ..core.progress import _queues, cleanup_job

logger = logging.getLogger(__name__)

ws_router = APIRouter()

STAGES = [
    ("uploading",  "Uploading files...",          10),
    ("parsing",    "Parsing PDF report...",        30),
    ("analyzing",  "Analyzing code structure...",  55),
    ("scoring",    "Calculating scores...",        75),
    ("feedback",   "Generating AI feedback...",    90),
]


@ws_router.websocket("/ws/evaluate/{job_id}")
async def evaluate_progress(websocket: WebSocket, job_id: str):
    """
    Real-time progress stream for an evaluation job.
    Client connects before submitting the form; server drains events until 'complete'/'error'.
    """
    await websocket.accept()
    logger.info(f"WebSocket connected for job: {job_id}")

    # Create a queue for this job if not yet created (client may connect first)
    from ..core.progress import create_job, _queues
    if job_id not in _queues:
        create_job(job_id)

    try:
        while True:
            try:
                # Poll queue with timeout so we can detect disconnects
                event = await asyncio.wait_for(_queues[job_id].get(), timeout=120.0)
                await websocket.send_text(json.dumps(event))

                # End the stream on terminal events
                if event.get("type") in ("complete", "error"):
                    break
            except asyncio.TimeoutError:
                # Send heartbeat to keep connection alive
                await websocket.send_text(json.dumps({"type": "heartbeat"}))
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for job: {job_id}")
    except Exception as e:
        logger.error(f"WebSocket error for job {job_id}: {e}")
        try:
            await websocket.send_text(json.dumps({"type": "error", "message": str(e)}))
        except Exception:
            pass
    finally:
        cleanup_job(job_id)
        logger.info(f"WebSocket cleanup done for job: {job_id}")
