import datetime
import logging

from telegram import Update, error
from telegram.ext import (
    CallbackContext,
    Filters,
    Job,
    JobQueue,
    MessageHandler,
    Updater,
)

import src.db as db
from src import settings
from src.schemas import Chat, Context

logger = logging.getLogger(__name__)


def add_job_to_queue(job_queue: JobQueue, chat: Chat):
    db.add_chat(chat=chat, active=True)
    job_queue.run_repeating(
        callback,
        10 if settings.DEBUG else settings.SECONDS_BETWEEN_CALLBACK,
        name=str(chat.id),
        context=Context(chat_id=chat.id),
    )


def remove_job_from_queue(job: Job, chat_id: int):
    print("removing job for chat id", chat_id)
    db.update_chat(chat_id=chat_id, active=False)
    job.remove()


def is_time_of_the_day() -> bool:
    if settings.DEBUG:
        return True
    now = datetime.datetime.now()
    time_of_the_day = db.get_time_of_the_day()
    return now.hour == time_of_the_day.hour and now.minute == time_of_the_day.minute


def callback(context: CallbackContext):
    if is_time_of_the_day():
        job_context: Context = context.job.context
        chat_id = job_context.chat_id
        try:
            context.bot.send_message(chat_id=chat_id, text=settings.CALLBACK_MESSAGE)
        except (error.Unauthorized, error.BadRequest):
            logger.error(f"bot is no longer part of chat {chat_id}")
            remove_job_from_queue(context.job, chat_id)


def new_member(update: Update, context: CallbackContext) -> None:
    members = [
        member
        for member in update.message.new_chat_members
        if member.username == settings.TELEGRAM_BOT_USERNAME
    ]
    bot_added_to_chat = len(members) > 0
    if bot_added_to_chat:
        print(update.message)
        chat = Chat.from_message(message=update.message, active=True)
        add_job_to_queue(context.job_queue, chat)
        update.message.reply_text(settings.WELCOME_MESSAGE)


def run():
    logger.info(f"starting telegram bot")
    updater = Updater(token=settings.TELEGRAM_TOKEN, use_context=True)
    for chat in db.get_chats(only_active=True):
        add_job_to_queue(updater.job_queue, chat)
    dispatcher = updater.dispatcher
    new_member_handler = MessageHandler(
        Filters.status_update.new_chat_members, new_member
    )
    dispatcher.add_handler(new_member_handler)
    updater.start_polling()
    updater.idle()
