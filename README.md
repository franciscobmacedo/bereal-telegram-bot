
# Telegram BeReal bot :robot:

A reminder bot to share a picture with your chat everyday at a random time. Heavily inspired by the app [Bereal](https://bere.al/en).

## To use it in your chat


<!--- This is currently running live so you can just add `@BeRealEverydayBot` to your chat and it will remind you to share a picture at a random time everyday.-->


:warning: This is currently not running live.


## For development

To setup locally:

1. On telegram, contact `@BotFather` to create a new bot and retrieve both your bot's username and the HTTP API token;
2. create an `.env` file, with environment variables, like it's in `.env.example` - add your bot's `TELEGRAM_BOT_USERNAME` and `TELEGRAM_TOKEN`;
3. Install dependencies with `poetry install`;
4. Launch a poetry shell so the dependencies are active: `poetry shell`;
5. Run `python run.py set-times <NUMBER_OF_DAYS> <MIN_HOUR> <MAX_HOUR>` to fill the times table with random times where:
   - `NUMBER_OF_DAYS` - **optional** - is the number of days that the bot will run for, starting today (default: 300);
   - `MIN_HOUR` - **optional** - is the earliest hour to send the message (default: 9);
   -  `MAX_HOUR` - **optional** - is the latest hour to send the message (default: 22);
6. Run `python run.py bot` to start the bot service;

You can also edit `src/settings.py` with your own preferences where:
1. `DEBUG`: variable to set if the command is always sent (if `True`) or only when the now time corresponds to the defined random time;
2. `SECONDS_BETWEEN_CALLBACK`: interval for the bot to check if the current time matches the random defined time - ignored in debug mode;
3. `WELCOME_MESSAGE`: message to send to the telegram chat when the bot joins the chat;
4. `CALLBACK_MESSAGE`: message to send to the telegram chat every day;
5. `DB_FILE`: where to store your chats and the random generated times;
6. `TIMES_TABLE_NAME`: the name of the DB table to store the random generated times;
7. `CHATS_TABLE_NAME`: the name of the DB table to store the chats ids;


