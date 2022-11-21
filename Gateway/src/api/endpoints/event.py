from fastapi import APIRouter, Request

from sse_starlette.sse import EventSourceResponse
import asyncio
from src.constants.const import System
from src.interfaces.core_interfaces.sse_adapter import EventQueue

router = APIRouter()


@router.get("/stream")
async def event_stream(request: Request):
    """
    Streams all events logs into the console which are created while the method is active
    :return: Line separated stream of events
    """
    queue = EventQueue.instance()
    return EventSourceResponse(queue.stream())
