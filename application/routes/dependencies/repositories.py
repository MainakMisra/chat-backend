from fastapi import Depends
from sqlalchemy.orm import Session

from application.database.repositories.users import UserRepository
from application.routes.dependencies.db import get_db_session


def get_user_repository(session: Session = Depends(get_db_session),) -> UserRepository:
    return UserRepository(session=session)
