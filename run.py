import typer

from src import settings
from src.bot import run
from src.db import create_times_of_the_day

app = typer.Typer()


@app.command()
def set_times(
    days: int = typer.Argument(settings.DAYS_TO_RUN),
    min_hour: int = typer.Argument(settings.MIN_HOUR),
    max_hour: int = typer.Argument(settings.MAX_HOUR),
):
    create_times_of_the_day(days, min_hour, max_hour)


@app.command()
def bot():
    run()


if __name__ == "__main__":
    app()
