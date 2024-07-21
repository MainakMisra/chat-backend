from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String,
                        UniqueConstraint, func)
from sqlalchemy.orm import relationship

from application.core.chat.serializers import Message
from application.core.users.serializers import User
from application.database.bases import Base


class UserOrm(Base):
    __tablename__ = "users"
    id: int = Column(Integer, primary_key=True)
    first_name: str = Column(String(100), nullable=False)
    last_name: str = Column(String(100), nullable=False)
    email: str = Column(String(100), nullable=False)
    password: str = Column(String(100), nullable=False)

    __table_args__ = (UniqueConstraint("email", "id", name="uix_email_id"),)

    messages = relationship("MessageOrm", back_populates="sender", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return (f"User(id={self.id}, "
                f"email={self.email})")

    def to_pydantic(self) -> User:
        return User(
            id=self.id,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
        )


class MessageOrm(Base):
    __tablename__ = "messages"
    id: int = Column(Integer, primary_key=True)
    sender_id: int = Column(Integer, ForeignKey('users.id'), nullable=False)
    content: str = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    sender: "UserOrm" = relationship("UserOrm", back_populates="messages")

    def __repr__(self) -> str:
        return f"Message(id={self.id}"

    def to_pydantic(self) -> Message:
        return Message(
            message_id=self.id,
            content=self.content,
            created_at=self.created_at,
            id=self.sender_id,
            first_name=self.sender.first_name,
            last_name=self.sender.last_name,
            email=self.sender.email
        )
