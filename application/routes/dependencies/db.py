import logging
from collections.abc import Generator

from fastapi import Depends, HTTPException, Request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from application.database import Database

logger = logging.getLogger(__name__)


# todo: to move this to an exception file
class UnexpectedInternalError(HTTPException):
    status_code = 500

    def __init__(self) -> None:
        self.detail = "Unexpected error on internal operation"


def get_db(request: Request) -> Database:
    try:
        db: Database = request.app.state.db
        return db
    except AttributeError:
        logger.exception("Internal error: 'request.app.state.db' unset for unknown reasons")
        raise UnexpectedInternalError


def get_db_session(database: Database = Depends(get_db), ) -> Generator[Session, None, None]:
    """Dependency used to create new database session for each request.

    Note: db object is passed as dependency injection to allow mocking it on
    tests.
    """
    session = database.Session()
    try:
        yield session
    except SQLAlchemyError:
        logger.exception("Caught unexpected database exception")
        raise UnexpectedInternalError
    finally:
        session.close()
