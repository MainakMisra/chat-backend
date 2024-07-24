from collections.abc import Callable

from fastapi.testclient import TestClient

from application.core.users.serializers import User, UserCreate, UserLogin


def test_existing_user_login(
    client: TestClient,
    api_url: str,
    create_user: Callable[[UserCreate], User],
    user_data: UserCreate,
) -> None:
    create_user(user_data)

    user_login_resp = client.request(
        method="post",
        url=f"{api_url}/auth/login",
        content=UserLogin(email=user_data.email, password=user_data.password).json(),
    )
    assert user_login_resp.status_code == 200


def test_get_logged_user(
    client: TestClient,
    api_url: str,
    get_logged_user_cookies: Callable[..., dict[str, str]],
    user_data: UserCreate,
) -> None:
    cookies = get_logged_user_cookies()

    response = client.request(
        method="get",
        url=f"{api_url}/users/me",
        cookies=cookies,
    )
    assert response.status_code == 200

    expected_user = User(**response.json()["data"])

    assert expected_user.email == user_data.email


def test_user_logout(
    client: TestClient,
    api_url: str,
    get_logged_user_cookies: Callable[..., dict[str, str]],
) -> None:
    cookies = get_logged_user_cookies()

    response = client.request(
        method="post",
        url=f"{api_url}/auth/logout",
        cookies=cookies,
    )
    assert response.status_code == 200
