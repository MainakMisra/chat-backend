from fastapi import Depends

from application.core.auth.service import AuthService
from application.core.chat.service import ChatService
from application.core.users.service import UserService
from application.database.repositories.chat import ChatRepository
from application.database.repositories.users import UserRepository
from application.routes.dependencies.repositories import (get_chat_repository,
                                                          get_user_repository)


def get_auth_service() -> AuthService:
    return AuthService()


def get_user_service(user_repository: UserRepository = Depends(get_user_repository), ) -> UserService:
    return UserService(user_repository=user_repository)


def get_chat_service(chat_repository: ChatRepository = Depends(get_chat_repository), ) -> ChatService:
    return ChatService(chat_repository=chat_repository)
