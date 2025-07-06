# backend/api/stream.py
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio

router = APIRouter()

async def event_stream():
	while True:
		yield f"data: ping\n\n"
		await asyncio.sleep(5)

@router.get("/stream")
async def stream():
	return StreamingResponse(event_stream(), media_type="text/event-stream")
