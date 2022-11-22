import datetime

from pydantic import BaseModel
from telegram import Message


class Chat(BaseModel):
    id: int
    title: str | None
    from_username: str | None
    from_is_bot: bool | None
    from_first_name: str | None
    from_last_name: str | None
    active: bool
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None

    @classmethod
    def from_message(cls, message: Message, active: bool = True):
        print("MESSAGE", message)
        print("chat", message.chat)
        print(message.from_user)
        return cls(
            id=message.chat.id,
            title=message.chat.title,
            from_username=message.from_user.username,
            from_is_bot=message.from_user.is_bot,
            from_first_name=message.from_user.first_name,
            from_last_name=message.from_user.last_name,
            active=active,
        )


class Context(BaseModel):
    chat_id: int
