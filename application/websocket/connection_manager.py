import logging
from typing import List

from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

from application.core.chat.serializers import Message


class ConnectionManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, websocket: WebSocket, message: Message):
        await websocket.send_json(message.json())

    async def broadcast(self, message: Message):
        try:
            for connection in self.active_connections:
                await connection.send_json(message.json())
        except WebSocketDisconnect:
            self.logger.info('websocket disconnected')


manager = ConnectionManager()
