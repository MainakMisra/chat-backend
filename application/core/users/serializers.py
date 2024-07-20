import re

from pydantic import BaseModel, EmailStr, Field, validator

# Regular expression for password
password_regex = re.compile("""[A-Za-z0-9.,?{}()-_+=!`~@#$%^&*|;'" ]{8,}$""")  # noqa: W605


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

    # @validator("password")
    # def password_regex_check(cls, v: str) -> str:
    #     if not password_regex.fullmatch(v):
    #         raise ValueError("password doesn't respect regex")
    #     return v


class UserPasswordUpdate(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    confirmation: str
    user_id: str
    email: str
