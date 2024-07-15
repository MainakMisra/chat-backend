import datetime
import re
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, validator

# password_regex = re.compile("""[A-Za-z0-9.,?{}()-_+=!`~@#$%^&*|;'" ]{8,}$""")  # noqa: W605
#
#
# class InvitedUser(BaseModel):
#     password: String100Char
#     token: str
#
#     @validator("password")
#     def password_regex_check(cls, v: str) -> str:
#         if not password_regex.fullmatch(v):
#             raise ValueError("password doesn't respect regex")
#         return v


class User(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str







