import logging

from application.base_classes import CallableInstance
from application.core.chat.serializers import Message
from application.database.repositories.chat import ChatRepository


class ChatService(CallableInstance):
    def __init__(
            self,
            chat_repository: ChatRepository,
    ) -> None:
        self.logger = logging.getLogger(__name__)
        self.chat_repository = chat_repository
        self.logger.debug("Chat service created")

    def insert_message(
            self, user_id: int, message: str
    ) -> Message:
        return self.chat_repository.insert_message(user_id=user_id, message=message)

    def get_messages(
            self,
    ) -> list[Message]:
        return self.chat_repository.get_messages()
