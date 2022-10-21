from typing import Optional

import typer

from src.bot import run
from src.db import create_times_of_the_day

app = typer.Typer()


@app.command()
def set_times(days: int = typer.Argument(300)):
    create_times_of_the_day(days)


@app.command()
def bot():
    run()


if __name__ == "__main__":
    app()
