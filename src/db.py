import datetime
import logging
import random
from typing import Optional

from tinydb import Query, operations

from src import settings

logger = logging.getLogger(__name__)


def create_times_of_the_day(days: int):
    logger.info(f"creating times for the next {days} days")
    table = settings.db.table(settings.TIMES_TABLE_NAME)
    table.truncate()
    today = datetime.date.today()
    for i in range(days):
        next_day = today + datetime.timedelta(days=i)
        hour = random.randint(10, 22)
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


def add_chat_id(chat_id: int, active: bool = True) -> None:
    query = Query()
    table = settings.db.table(settings.CHATS_TABLE_NAME)
    chat = table.search(query.chat_id == chat_id)
    if chat:
        logger.info(
            f"chat_id {chat_id} is already in the database - updating active status to {active}"
        )
        table.update(operations.set("active", active), query.chat_id == chat_id)
        return
    logger.info(f"Adding chat_id {chat_id}")
    table.insert({"chat_id": chat_id, "active": active})
    logger.info(f"Done!")


def disable_chat_id(chat_id: int) -> None:
    query = Query()
    table = settings.db.table(settings.CHATS_TABLE_NAME)
    logger.info(f"Disabling chat_id {chat_id}")
    table.update(operations.set("active", False), query.chat_id == chat_id)
    logger.info(f"Done!")


def get_chat_ids(only_active: bool = True) -> list[int]:
    logger.info(f"Getting {'active' if only_active else 'all'} chats")
    table = settings.db.table(settings.CHATS_TABLE_NAME)
    chats = table.all()
    logger.info(f"Found {len(chats)} chats")
    return [chat["chat_id"] for chat in chats]
