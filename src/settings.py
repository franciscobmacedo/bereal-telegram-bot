import logging

from decouple import config
from tinydb import TinyDB

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)

DEBUG = config("DEBUG", cast=bool)

# Bot
TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
TELEGRAM_BOT_USERNAME = config("TELEGRAM_BOT_USERNAME")
SECONDS_BETWEEN_CALLBACK = 60

WELCOME_MESSAGE = """
Thank you for adding me to your chat! I will send a message to this chat at a random time every day with a reminder to share a picture.
"""

CALLBACK_MESSAGE = """
📸  It's time for your picture of the day!

Send a picture of what you are doing right now 🐭
"""

# Database
DB_FILE = "db.json"
TIMES_TABLE_NAME = "times"
CHATS_TABLE_NAME = "chats"

db = TinyDB(DB_FILE)

DAYS_TO_RUN = 300
MIN_HOUR = 9
MAX_HOUR = 22
