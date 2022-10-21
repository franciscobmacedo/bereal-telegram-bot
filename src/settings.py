import logging

from decouple import config
from tinydb import TinyDB

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)

# Bot
TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
TELEGRAM_BOT_USERNAME = config("TELEGRAM_BOT_USERNAME")
SECONDS_BETWEEN_CALLBACK = 60
MESSAGE = """
📸  It's time for your picture of the day!

Send a picture of what you are doing right now 🐭
"""

# Database
DB_FILE = "db.json"
TIMES_TABLE_NAME = "times"
CHATS_TABLE_NAME = "chats"

db = TinyDB(DB_FILE)
