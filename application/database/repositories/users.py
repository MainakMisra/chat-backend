import logging

from sqlalchemy.orm import Session

from application.core.serializers.user import User
from application.core.users.serializers import UserCreate
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
