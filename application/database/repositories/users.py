import logging

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from application.core.users.exceptions import UserEmailNotFound, UserIdNotFound
from application.core.users.serializers import User, UserCreate
from application.database.models.users import UserOrm


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.logger = logging.getLogger(__name__)
        self.session = session

    def insert_user(self, user_to_insert: UserCreate) -> User:
        self.logger.info(f"Inserting user with email='{user_to_insert.email}'")
        new_user_orm = UserOrm(**user_to_insert.dict())

        self.session.add(new_user_orm)
        self.session.commit()
        self.session.refresh(new_user_orm)

        return new_user_orm.to_pydantic()

    def user_with_email_exists(self, user_email: str) -> bool:
        self.logger.info(f"Checking that a user with email='{user_email}' exists")
        return self.session.query(UserOrm.id).filter_by(email=user_email).first() is not None

    def get_user_by_email(self, user_email: str) -> User:
        self.logger.info(f"Checking that a user with email='{user_email}' exists")
        try:
            user: User = (
                self.session.query(UserOrm).filter_by(email=user_email).one().to_pydantic()
            )
        except NoResultFound:
            self.logger.exception(f"Didn't find user with email '{user_email}'")
            raise UserEmailNotFound(user_email=user_email)

        return user

    def get_user_by_id(self, user_id: int) -> User:
        self.logger.info(f"Checking that a user with id='{user_id}' exists")
        try:
            user: User = (
                self.session.query(UserOrm).filter_by(id=user_id).one().to_pydantic()
            )
        except NoResultFound:
            self.logger.exception(f"Didn't find user with id '{user_id}'")
            raise UserIdNotFound(user_id=user_id)

        return user

    def update_password(self, user_id: int, new_password: str) -> None:
        self.logger.info(f"Updating password for user with id='{user_id}'")
        self.session.query(UserOrm).filter_by(id=user_id).update({"password": new_password})
        self.session.commit()
