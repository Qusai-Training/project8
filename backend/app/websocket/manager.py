from typing import List, Dict, Any
from fastapi import WebSocket


class ConnectionManager:
    """Manages active WebSocket connections and broadcasts events."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accepts and tracks a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Removes a disconnected WebSocket connection from tracking."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, event_type: str, payload: Dict[str, Any]):
        """Broadcasts a structured event and payload to all connected clients."""
        message = {
            "event": event_type,
            "data": payload
        }
        
        # Iterate over a copy to safely remove dead connections during iteration
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception:
                self.disconnect(connection)


# Global connection manager instance
manager = ConnectionManager()