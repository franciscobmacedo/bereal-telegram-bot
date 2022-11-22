from multiprocessing import Process

import typer
import uvicorn

from src import settings
from src.bot import run as run_bot
from src.db import create_times_of_the_day

app = typer.Typer()


def run_dashboard():
    uvicorn.run("src.dashboard:app", host="0.0.0.0", port=8040, reload=True)


@app.command()
def set_times(
    days: int = typer.Argument(
        settings.DAYS_TO_RUN,
        help="The number of days that the bot will run for, starting today.",
    ),
    min_hour: int = typer.Argument(
        settings.MIN_HOUR, help="The earliest hour to send the message."
    ),
    max_hour: int = typer.Argument(
        settings.MAX_HOUR, help="The latest hour to send the message."
    ),
):
    create_times_of_the_day(days, min_hour, max_hour)


@app.command()
def bot():
    run_bot()


@app.command()
def dashboard():
    run_dashboard()


@app.command()
def both():
    bot_process = Process(target=run_bot)
    bot_process.start()

    dashboard_process = Process(target=run_dashboard)
    dashboard_process.start()


if __name__ == "__main__":
    app()
