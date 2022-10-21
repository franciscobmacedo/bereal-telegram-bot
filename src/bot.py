import datetime
import logging

from pydantic import BaseModel
from telegram import Update, error
from telegram.ext import (CallbackContext, Filters, Job, JobQueue,
                          MessageHandler, Updater)

import src.db as db
from src import settings


class Context(BaseModel):
    chat_id: int


logger = logging.getLogger(__name__)


def add_job_to_queue(job_queue: JobQueue, chat_id: int):
    db.add_chat_id(chat_id)
    job_queue.run_repeating(
        callback,
        settings.SECONDS_BETWEEN_CALLBACK,
        name=str(chat_id),
        context=Context(chat_id=chat_id),
    )


def remove_job_from_queue(job: Job, chat_id: int):
    db.disable_chat_id(chat_id)
    job.remove()


def is_time_of_the_day() -> bool:
    # for debugging
    # return True
    now = datetime.datetime.now()
    time_of_the_day = db.get_time_of_the_day()
    return now.hour == time_of_the_day.hour and now.minute == time_of_the_day.minute


def callback(context: CallbackContext):
    if is_time_of_the_day():
        job_context: Context = context.job.context
        chat_id = job_context.chat_id
        try:
            context.bot.send_message(chat_id=chat_id, text=settings.MESSAGE)
        except error.Unauthorized:
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
        add_job_to_queue(context.job_queue, update.message.chat_id)
        update.message.reply_text(
            "Be Real Bot was added! It will send a message to this chat at a random time each day for you to to post a picture with a window of 2 minutes!"
        )


def run():
    logger.info(f"starting telegram bot")
    updater = Updater(token=settings.TELEGRAM_TOKEN, use_context=True)
    for chat_id in db.get_chat_ids():
        add_job_to_queue(updater.job_queue, chat_id)
    dispatcher = updater.dispatcher
    new_member_handler = MessageHandler(
        Filters.status_update.new_chat_members, new_member
    )
    dispatcher.add_handler(new_member_handler)
    updater.start_polling()
    updater.idle()
