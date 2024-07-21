import logging

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from application.core.chat.serializers import Message
from application.core.users.exceptions import UserIdNotFound
from application.database.models.users import MessageOrm, UserOrm


class ChatRepository:
    def __init__(self, session: Session) -> None:
        self.logger = logging.getLogger(__name__)
        self.session = session

    def insert_message(self, user_id: int, message: str) -> Message:
        try:
            user: UserOrm = (
                self.session.query(UserOrm).filter_by(id=user_id).one()
            )
        except NoResultFound:
            self.logger.exception(f"Didn't find user with id '{user_id}'")
            raise UserIdNotFound(user_id=user_id)

        new_message = MessageOrm(
            content=message,
            sender=user
        )

        self.session.add(new_message)
        self.session.commit()
        self.session.refresh(new_message)

        return new_message.to_pydantic()

    def get_messages(self, ) -> list[Message]:
        messages = self.session.query(MessageOrm).all()
        return [message.to_pydantic() for message in messages]
