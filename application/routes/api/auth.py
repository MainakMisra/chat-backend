import logging

from fastapi import Depends, Response, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from application.base_classes import APIRouter
from application.core.auth.jwt_config import Settings
from application.core.auth.security import SecurityService
from application.core.auth.service import AuthService
from application.core.serializers.response import ApiResponse
from application.core.users.serializers import UserLogin, UserLoginResponse
from application.routes.dependencies.db import get_db_session
from application.routes.dependencies.services import get_auth_service

logger = logging.getLogger(__name__)
AUTH_RESOURCE = "auth"

router = APIRouter(
    prefix=f"/{AUTH_RESOURCE}",
    tags=[AUTH_RESOURCE],
)


@AuthJWT.load_config
def get_config() -> Settings:
    return Settings()


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[UserLoginResponse],
)
async def login(
        user_login: UserLogin,
        auth_service: AuthService = Depends(get_auth_service),
        security_service: SecurityService = Depends(SecurityService),
        session: Session = Depends(get_db_session),
) -> ApiResponse[UserLoginResponse]:

    res = auth_service.login(login_details=user_login, session=session)

    security_service.set_login_cookies(user_id=res.user_id)

    return ApiResponse[UserLoginResponse](data=res)


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
        response: Response,
        security_service: SecurityService = Depends(SecurityService),
) -> Response:

    security_service.remove_cookies()
    logger.info("jwt tokens removed")
    response.status_code = 200

    return response
