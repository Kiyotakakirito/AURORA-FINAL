"""
Progress event bus for real-time WebSocket evaluation updates.
Each job_id maps to an asyncio.Queue of progress events.
"""
import asyncio
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

# Global registry: job_id -> asyncio.Queue
_queues: Dict[str, asyncio.Queue] = {}


def create_job(job_id: str) -> asyncio.Queue:
    """Create a new progress queue for the given job_id."""
    q: asyncio.Queue = asyncio.Queue()
    _queues[job_id] = q
    logger.info(f"Progress queue created for job: {job_id}")
    return q


async def send_progress(job_id: str, stage: str, message: str, percent: int, data: Any = None) -> None:
    """
    Push a progress event into the job's queue.
    Stages: 'uploading' | 'parsing' | 'analyzing' | 'scoring' | 'feedback' | 'complete' | 'error'
    """
    q = _queues.get(job_id)
    if q is None:
        logger.warning(f"No queue found for job: {job_id}")
        return
    event = {
        "type": "progress",
        "stage": stage,
        "message": message,
        "percent": percent,
        "data": data,
    }
    await q.put(event)


async def send_complete(job_id: str, result: Any) -> None:
    """Push final completion event with full evaluation result."""
    q = _queues.get(job_id)
    if q is None:
        return
    await q.put({"type": "complete", "stage": "complete", "percent": 100, "data": result})


async def send_error(job_id: str, message: str) -> None:
    """Push an error event."""
    q = _queues.get(job_id)
    if q is None:
        return
    await q.put({"type": "error", "stage": "error", "message": message, "percent": 0})


def cleanup_job(job_id: str) -> None:
    """Remove the queue after the WebSocket disconnects."""
    _queues.pop(job_id, None)
    logger.info(f"Progress queue cleaned up for job: {job_id}")
