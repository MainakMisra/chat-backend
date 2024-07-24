from collections.abc import AsyncGenerator, Generator
from contextlib import asynccontextmanager
from os.path import dirname

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists, drop_database

from application.app import init_app
from application.config import Settings
from application.database import Database


@pytest.fixture(scope="session")
def project_root_dir() -> str:
    return dirname(dirname(__file__))


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings()


@pytest.fixture(scope="package")
def base_db_uri(settings: Settings) -> str:
    return (
        f"postgresql://{settings.db_uri.user}"
        f":{settings.db_uri.password}"
        f"@{settings.db_uri.host}"
        f"{f':{settings.db_uri.port}' if settings.db_uri.port else ''}"
        f"/chat_test"
    )


@pytest.fixture(scope="package")
def database(
    base_db_uri: str,
) -> Database:
    database = Database(db_uri=base_db_uri)
    if database_exists(base_db_uri):
        drop_database(base_db_uri)

    create_database(base_db_uri)

    database.initialize_tables()
    return database


@pytest.fixture(scope="function")
def session(database: Database) -> Generator[Session, None, None]:
    session = database.Session()
    yield session
    session.close()


@pytest.fixture(scope="package")
def app(
    settings: Settings,
    database: Database,
) -> FastAPI:
    @asynccontextmanager
    async def custom_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        app.state.db = database

        # Run server
        yield

    app = init_app()

    return app


@pytest.fixture(scope="package")
def client(app: FastAPI) -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function", autouse=True)
def clean_db(database: Database) -> Generator[None, None, None]:
    database.truncate_db()
    yield
