from fastapi import HTTPException

from application.core.exceptions import CoreBaseException


class UserWithEmailAlreadyExists(CoreBaseException):
    def __init__(self, user_email: str) -> None:
        self.details = f"A user with this email address '{user_email}' already exists."


class UserEmailNotFound(CoreBaseException):
    def __init__(self, user_email: str) -> None:
        self.details = f"No user with email='{user_email}' exists."


class UserIdNotFound(CoreBaseException):
    def __init__(self, user_id: int) -> None:
        self.details = f"No user with id='{user_id}' exists."


class HTTPUserAlreadyExists(HTTPException):
    status_code = 409

    def __init__(self, user_email: str) -> None:
        self.detail = f"User with email '{user_email}' already exists."


class HTTPUserNotFound(HTTPException):
    status_code = 404

    def __init__(self, user_email: str | None = None) -> None:
        self.detail = f"User with email '{user_email}' does not exists."
