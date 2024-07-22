from unittest.mock import MagicMock

import pytest

from application.core.users.exceptions import UserWithEmailAlreadyExists
from application.core.users.serializers import UserCreate
from application.core.users.service import UserService


def test_insert_user_fails_if_user_with_same_email_exists() -> None:
    user_email = "test@test.com"
    user_to_create = UserCreate(
        email=user_email,
        password="R@nd0mP@ssw0rd",
        first_name="first_name",
        last_name="last_name",
    )
    mock_user_repository = MagicMock()
    user_service = UserService(user_repository=mock_user_repository)

    mock_user_repository.user_with_email_exists.return_value = True

    with pytest.raises(UserWithEmailAlreadyExists):
        user_service.insert_user(user_to_create=user_to_create)

    mock_user_repository.user_with_email_exists.assert_called_once_with(
        user_email=user_email
    )


def test_insert_user_is_successful_when_user_does_not_exist() -> None:
    user_email = "test@test.com"
    user_to_create = UserCreate(
        email=user_email,
        permission="emp",
        password="R@nd0mP@ssw0rd",
        first_name="first_name",
        last_name="last_name",
    )
    mock_user_repository = MagicMock()
    user_service = UserService(user_repository=mock_user_repository)

    mock_user_repository.user_with_email_exists.return_value = False

    user_service.insert_user(user_to_create=user_to_create)

    mock_user_repository.user_with_email_exists.insert_user(
        user_to_insert=user_to_create
    )


#
# def test_update_password_fails_if_user_does_not_exists() -> None:
#     # Test data setup
#     user_id = 1
#     new_password = "R@nd0mP@ssw0rd"
#
#     mock_user_repository = MagicMock()
#     # SUT
#     user_service = UserService(user_repository=mock_user_repository)
#
#     # Mock setup
#     mock_user_repository.user_with_id_exists.return_value = False
#
#     # Test behavior
#     with pytest.raises(UserIdNotFound):
#         user_service.update_user_password(user_id=user_id, new_password=new_password)
#
#     mock_user_repository.user_with_id_exists.assert_called_once_with(user_id=user_id)
#
#
# def test_update_password_is_successful_when_user_exists() -> None:
#     # Test data setup
#     user_id = 1
#     new_password = "R@nd0mP@ssw0rd"
#
#     mock_user_repository = MagicMock()
#     # SUT
#     user_service = UserService(user_repository=mock_user_repository)
#
#     # Mock setup
#     mock_user_repository.user_with_id_exists.return_value = True
#
#     # Test behavior
#     user_service.update_user_password(user_id=user_id, new_password=new_password)
#
#     # TODO: call arguments must also be tested but that's only possible if the hashing is correctly injected into the service to be able to mock it
#     mock_user_repository.update_password.assert_called_once
