from fastapi import Depends

from application.core.users.service import UserService
from application.database.repositories.users import UserRepository
from application.routes.dependencies.repositories import get_user_repository


def get_user_service(user_repository: UserRepository = Depends(get_user_repository) ,) -> UserService:
    return UserService(user_repository=user_repository)
