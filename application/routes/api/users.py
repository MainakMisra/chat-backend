import logging

from fastapi import Depends, status

from application.base_classes import APIRouter
from application.core.serializers.response import ApiResponse
from application.core.serializers.user import User
from application.core.users.exceptions import (HTTPUserAlreadyExists,
                                               UserWithEmailAlreadyExists)
from application.core.users.serializers import UserCreate
from application.core.users.service import UserService
from application.routes.dependencies.services import get_user_service

logger = logging.getLogger(__name__)

USER_RESOURCE = "users"

router = APIRouter(
    prefix=f"/{USER_RESOURCE}",
    tags=[USER_RESOURCE],
)


@router.post(
    "/create-user",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[User],
)
async def create_invited_user(
    user_details: UserCreate,
    user_service: UserService = Depends(get_user_service),
) -> ApiResponse[User]:

    try:
        user = user_service.insert_user(
            user_to_create=user_details
        )
    except UserWithEmailAlreadyExists:
        raise HTTPUserAlreadyExists(user_email=user_details.email)

    return ApiResponse[User](data=user)