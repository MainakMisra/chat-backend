from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from application.core.chat.serializers import Message
from application.core.chat.service import ChatService
from application.routes.dependencies.services import get_chat_service
from application.websocket.connection_manager import manager

router = APIRouter(prefix="/ws")


@router.websocket("/{client_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        client_id: int,
        chat_service: ChatService = Depends(get_chat_service),
):
    await manager.connect(websocket)

    messages = chat_service.get_messages()

    for message in messages:
        await manager.send_personal_message(websocket=websocket, message=message)
    try:
        while True:
            data = await websocket.receive_text()

            message: Message = chat_service.insert_message(user_id=client_id, message=data)

            await manager.send_personal_message(websocket=websocket, message=message)

            await manager.broadcast(message=message)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
