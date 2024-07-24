from typing import Callable, cast

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from application.config import Settings
from application.core.users.serializers import User, UserCreate, UserLogin
from application.core.users.service import UserService
from application.database.repositories.users import UserRepository
from application.routes.dependencies.services import get_user_service


@pytest.fixture(scope="package")
def api_url(settings: Settings) -> str:
    return settings.api_prefix


@pytest.fixture(scope="function")
def user_service(app: FastAPI, session: Session) -> UserService:
    try:
        user_service = app.dependency_overrides[get_user_service]
    except KeyError:
        user_service = UserService(user_repository=UserRepository(session=session))
    return cast(UserService, user_service)


@pytest.fixture(scope="function")
def user_data() -> UserCreate:
    return UserCreate(
        email="test@gmail.com",
        password="123",
        first_name="first_name",
        last_name="last_name",
    )


@pytest.fixture(scope="function")
def create_user(
    session: Session, user_service: UserService
) -> Callable[[UserCreate], User]:
    def create_user(
        user: UserCreate,
    ) -> User:
        user_created = user_service.insert_user(
            user_to_create=UserCreate(**user.dict()),
        )
        return user_created

    return create_user


@pytest.fixture(scope="function")
def get_logged_user_cookies(
    api_url: str,
    client: TestClient,
    user_data: UserCreate,
) -> Callable[..., dict[str, str]]:
    def get_logged_user_cookies() -> dict[str, str]:
        response = client.request(
            method="post",
            url=f"{api_url}/auth/login",
            content=UserLogin(
                email=user_data.email, password=user_data.password
            ).json(),
        )
        return dict(response.cookies)

    return get_logged_user_cookies
