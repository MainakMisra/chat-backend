from datetime import datetime

from application.core.users.serializers import User


class Message(User):
    message_id: int
    content: str
    created_at: datetime
