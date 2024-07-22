import logging

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import check_password_hash

from application.base_classes import CallableInstance
from application.core.users.exceptions import HTTPUserNotFound
from application.core.users.serializers import UserLogin, UserLoginResponse
from application.database.models.users import UserOrm
from application.routes.api.exceptions import UserPasswordMisMatch


class AuthService(CallableInstance):
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.info("Authentication service initialized")

    def login(self, login_details: UserLogin, session: Session) -> UserLoginResponse:
        self.logger.info(f"Logging in user {login_details.email}")
        try:
            user_data = (
                session.query(UserOrm).filter_by(email=login_details.email).one()
            )

        except NoResultFound:
            raise HTTPUserNotFound(user_email=login_details.email)

        if check_password_hash(user_data.password, login_details.password) is True:
            return UserLoginResponse(
                confirmation="correct",
                user_id=str(user_data.id),
                email=user_data.email,
            )
        raise UserPasswordMisMatch()
