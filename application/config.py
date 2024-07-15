from os.path import dirname, realpath
from typing import Literal

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    # Server's internal behavior
    # server_host: str = "0.0.0.0"
    api_prefix: str = "/api"
    server_port: int = 9000
    uvicorn_auto_reload: bool = True

    # Logging
    logging_json_format: bool = False
    logging_level: Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"] = "INFO"
    sqlalchemy_log_level: Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"] = "WARNING"

    # Postgres' configuration for db used by the server and by pytest
    db_uri: PostgresDsn

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    backend_cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost",
    ]
    backend_cors_origin_regex: str | None = None

    # Application's frontend related parameters
    application_protocol: Literal["https", "http"] = "https"
    application_host: str

    app_name: str = "chat-backend"

    @validator("backend_cors_origins", pre="before")
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        env_file = f"{dirname(dirname(realpath(__file__)))}/config/server.env"
        env_file_encoding = "utf-8"
        # Allow variables to be defined in lower case inside the ide and
        # upper case on environment variables
        case_sensitive = False


# Settings become accessible as "singleton" created only once on module import
settings = Settings()
