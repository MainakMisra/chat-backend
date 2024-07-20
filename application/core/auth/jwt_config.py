from pydantic import BaseModel


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_token_location: set[str] = {"cookies"}
    authjwt_cookie_secure: bool = True
    authjwt_cookie_samesite: str = "none"
    authjwt_cookie_httponly: bool = True
    authjwt_cookie_csrf_protect: bool = False
