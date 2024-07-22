from os.path import dirname

import pytest
from sqlalchemy_utils import create_database, database_exists, drop_database

from application.config import Settings
from application.database import Database


@pytest.fixture(scope="session")
def project_root_dir() -> str:
    return dirname(dirname(__file__))


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings()


@pytest.fixture(scope="session")
def base_db_uri(settings: Settings) -> str:
    return (
        f"postgresql://{settings.db_uri.user}"
        f":{settings.db_uri.password}"
        f"@{settings.db_uri.host}"
        f"{f':{settings.db_uri.port}' if settings.db_uri.port else ''}"
    )


@pytest.fixture(scope="session")
def fake_data_db_uri(base_db_uri: str) -> str:
    """Url connection for application tests."""
    return f"{base_db_uri}/chat_test_application"


@pytest.fixture(scope="session")
def fake_data_db(fake_data_db_uri: str) -> Database:
    db = Database(db_uri=fake_data_db_uri)
    # Ensure that database is created and filled
    if database_exists(db.db_uri):
        drop_database(db.db_uri)

    # Ensure that db exists
    create_database(db.db_uri)

    # Create database schema
    db.initialize_tables()
    return db
