from fastapi import HTTPException


class UserIdCookieNotPresent(HTTPException):
    status_code: int = 404

    def __init__(self) -> None:
        self.detail = "user id is missing in cookies !"


class UserIdNotPresent(HTTPException):
    status_code: int = 404

    def __init__(self) -> None:
        self.detail = "user id not present !"


class UserPasswordMisMatch(HTTPException):
    status_code = 401

    def __init__(self, ) -> None:
        self.detail = "user password mismatch error"


class UnauthorizedUserError(HTTPException):
    status_code: int = 401

    def __init__(self, ) -> None:
        self.detail = "User authentication failed."
