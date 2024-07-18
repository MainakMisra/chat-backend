from fastapi import HTTPException

from application.core.exceptions import CoreBaseException


class UserWithEmailAlreadyExists(CoreBaseException):
    def __init__(self, user_email: str) -> None:
        self.details = f"A user with this email address '{user_email}' already exists."


class HTTPUserAlreadyExists(HTTPException):
    status_code = 409

    def __init__(self, user_email: str) -> None:
        self.detail = f"User with email '{user_email}' already exists."
