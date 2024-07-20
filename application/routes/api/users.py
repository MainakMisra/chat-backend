import logging

from fastapi import Depends, status

from application.base_classes import APIRouter
from application.core.serializers.response import ApiResponse
from application.core.users.exceptions import (HTTPUserAlreadyExists,
                                               HTTPUserNotFound,
                                               UserEmailNotFound,
                                               UserWithEmailAlreadyExists)
from application.core.users.serializers import (User, UserCreate,
                                                UserPasswordUpdate)
from application.core.users.service import UserService
from application.routes.dependencies.security import get_current_user
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


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[User],
)
async def get_current_active_user(
    user: User = Depends(get_current_user),
) -> ApiResponse[User]:

    return ApiResponse[User](
        data=user
    )


@router.put(
    "/me/password",
    status_code=status.HTTP_200_OK,
)
async def update_password(
    user_password_update: UserPasswordUpdate,
    user_service: UserService = Depends(get_user_service),
) -> None:

    try:
        user = user_service.get_user_by_email(user_email=user_password_update.email)
    except UserEmailNotFound:
        raise HTTPUserNotFound(user_email=user_password_update.email)

    user_service.update_user_password(
        user_id=user.id,
        new_password=user_password_update.password,
    )
