# backend/app/api/websocket.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from app.core.websocket import manager
from app.core.deps import get_current_user_websocket
from app.models.user import User
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(None)
):
    """WebSocket endpoint for real-time updates."""
    
    user = None
    user_id = None
    
    # Authenticate user if token provided
    if token:
        try:
            user = await get_current_user_websocket(token)
            user_id = str(user.id) if user else None
        except Exception as e:
            logger.error(f"WebSocket authentication failed: {e}")
            await websocket.close(code=1008)  # Policy violation
            return
    
    await manager.connect(websocket, user_id)
    
    try:
        # Send welcome message
        await manager.send_personal_message(
            '{"type": "connected", "message": "Connected to Issues & Insights Tracker"}',
            websocket
        )
        
        # Keep connection alive and handle incoming messages
        while True:
            data = await websocket.receive_text()
            
            # Handle ping/pong for connection health
            if data == "ping":
                await manager.send_personal_message("pong", websocket)
            
            # You can add more message handling here
            logger.info(f"Received message from {user_id or 'anonymous'}: {data}")
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        logger.info(f"User {user_id or 'anonymous'} disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket, user_id)