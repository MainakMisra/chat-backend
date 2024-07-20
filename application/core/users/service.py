import logging

from werkzeug.security import generate_password_hash

from application.base_classes import CallableInstance
from application.core.users.exceptions import UserWithEmailAlreadyExists
from application.core.users.serializers import User, UserCreate
from application.database.repositories.users import UserRepository


class UserService(CallableInstance):
    def __init__(
            self,
            user_repository: UserRepository,
    ) -> None:
        self.logger = logging.getLogger(__name__)
        self.user_repository = user_repository
        self.logger.debug("User service created")

    def insert_user(
            self,
            user_to_create: UserCreate,
    ) -> User:
        self.logger.info(f"Creating new user with email {user_to_create.email}")

        if self.user_repository.user_with_email_exists(user_email=user_to_create.email):
            self.logger.error(f"A user with the email '{user_to_create.email}' already exists. Abort user creation.")
            raise UserWithEmailAlreadyExists(user_email=user_to_create.email)

        user_to_create.password = generate_password_hash(user_to_create.password, method="sha256")

        created_user = self.user_repository.insert_user(user_to_insert=user_to_create)

        return created_user

    def get_user_by_email(
            self,
            user_email: str,
    ) -> User:
        return self.user_repository.get_user_by_email(user_email=user_email)

    def update_user_password(self, user_id: int, new_password: str) -> None:

        self.logger.info(f"Updating user password for user with id {user_id}")
        hashed_password = generate_password_hash(new_password, method="sha256")

        self.user_repository.update_password(user_id=user_id, new_password=hashed_password)
