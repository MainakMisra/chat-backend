from fastapi import Depends
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from application.core.auth.security import SecurityService
from application.core.users.serializers import User
from application.database.models.users import UserOrm
from application.routes.api.exceptions import (UserIdCookieNotPresent,
                                               UserIdNotPresent)
from application.routes.dependencies.db import get_db_session


def get_current_user(
    auth: SecurityService = Depends(SecurityService),
    session: Session = Depends(get_db_session),
) -> User:
    user_id = auth.authenticate(session)

    if user_id is None:
        raise UserIdCookieNotPresent

    try:
        user_data: UserOrm = (session.query(UserOrm).filter_by(id=user_id).one())
    except NoResultFound:
        raise UserIdNotPresent

    return user_data.to_pydantic()

