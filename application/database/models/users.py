from sqlalchemy import Column, Integer, String, UniqueConstraint

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