# backend/app/core/websocket.py

from fastapi import WebSocket
from typing import List, Dict
import json
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str = None):
        await websocket.accept()
        self.active_connections.append(websocket)
        
        if user_id:
            if user_id not in self.user_connections:
                self.user_connections[user_id] = []
            self.user_connections[user_id].append(websocket)
        
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket, user_id: str = None):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        
        if user_id and user_id in self.user_connections:
            if websocket in self.user_connections[user_id]:
                self.user_connections[user_id].remove(websocket)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]
        
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")

    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients."""
        if self.active_connections:
            message_str = json.dumps(message)
            disconnected = []
            
            for connection in self.active_connections:
                try:
                    await connection.send_text(message_str)
                except Exception as e:
                    logger.error(f"Error broadcasting to connection: {e}")
                    disconnected.append(connection)
            
            # Remove disconnected connections
            for connection in disconnected:
                self.disconnect(connection)

    async def broadcast_to_user(self, message: dict, user_id: str):
        """Broadcast message to specific user's connections."""
        if user_id in self.user_connections:
            message_str = json.dumps(message)
            disconnected = []
            
            for connection in self.user_connections[user_id]:
                try:
                    await connection.send_text(message_str)
                except Exception as e:
                    logger.error(f"Error broadcasting to user {user_id}: {e}")
                    disconnected.append(connection)
            
            # Remove disconnected connections
            for connection in disconnected:
                self.disconnect(connection, user_id)

    async def notify_issue_created(self, issue_data: dict):
        """Notify all users about new issue creation."""
        await self.broadcast({
            "type": "issue_created",
            "data": issue_data,
            "timestamp": issue_data.get("created_at")
        })

    async def notify_issue_updated(self, issue_data: dict, updated_by: str):
        """Notify all users about issue updates."""
        await self.broadcast({
            "type": "issue_updated",
            "data": issue_data,
            "updated_by": updated_by,
            "timestamp": issue_data.get("updated_at")
        })

    async def notify_issue_deleted(self, issue_id: str, deleted_by: str):
        """Notify all users about issue deletion."""
        await self.broadcast({
            "type": "issue_deleted",
            "issue_id": issue_id,
            "deleted_by": deleted_by
        })

# Global connection manager instance
manager = ConnectionManager()