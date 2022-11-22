import datetime
import logging
import random
from typing import Optional

from pydantic import parse_obj_as
from tinydb import Query

from src import settings
from src.schemas import Chat

logger = logging.getLogger(__name__)


def now():
    return datetime.datetime.now().isoformat()


def create_times_of_the_day(days: int, min_hour: int, max_hour: int):
    logger.info(
        f"creating random times for the next {days} days between {min_hour}h and {max_hour}h."
    )

    table = settings.db.table(settings.TIMES_TABLE_NAME)
    table.truncate()
    today = datetime.date.today()
    for i in range(days):
        next_day = today + datetime.timedelta(days=i)
        hour = random.randint(min_hour, max_hour)
        minute = random.randint(0, 59)
        table.insert(
            {
                "date": next_day.isoformat(),
                "time": datetime.time(hour, minute).isoformat(),
            }
        )
    logger.info(f"Done!")


def get_time_of_the_day() -> Optional[datetime.time]:
    query = Query()
    table = settings.db.table(settings.TIMES_TABLE_NAME)
    now = datetime.datetime.now().date().isoformat()
    times = table.search(query.date == now)
    if times:
        return datetime.time.fromisoformat(times[0]["time"])


def add_chat(chat: Chat, active: bool = True) -> None:
    query = Query()
    table = settings.db.table(settings.CHATS_TABLE_NAME)
    if table.search(query.id == chat.id):
        logger.info(
            f"chat_id {chat.id} is already in the database - updating active status to {active}"
        )
        update_chat(chat=chat, active=active)
        return
    logger.info(f"Adding chat_id {chat.id}")
    chat.updated_at = now()
    chat.created_at = now()
    chat.active = active
    table.insert(chat.dict())
    logger.info(f"Done!")


def update_chat(
    chat: Chat | None = None, chat_id: int | None = None, active: bool = True
) -> None:
    query = Query()
    table = settings.db.table(settings.CHATS_TABLE_NAME)
    if chat_id:
        chat_obj = table.search(query.id == chat_id)[0]
        chat = Chat.parse_obj(chat_obj)
    elif not chat:
        raise Exception("chat_id or chat object are needed to update db")
    logger.info(f"updating chat_id {chat.id}")
    table.update({"active": active, "updated_at": now()}, query.id == chat.id)
    logger.info(f"Done!")


def get_chats(only_active: bool = True) -> list[Chat]:
    logger.info(f"Getting {'active' if only_active else 'all'} chats")
    table = settings.db.table(settings.CHATS_TABLE_NAME)
    chats_arr = table.all()
    chats = parse_obj_as(list[Chat], chats_arr)
    logger.info(f"Found {len(chats)} chats in total")
    if only_active:
        return [chat for chat in chats if chat.active == True]
    return chats


def get_chat_ids(only_active: bool = True) -> list[int]:
    chats = get_chats(only_active)
    return [chat.id for chat in chats]
