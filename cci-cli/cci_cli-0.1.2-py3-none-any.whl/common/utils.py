from enum import Enum
import sys
from typing import Dict

import confuse
import typer

APP_NAME = "circleci-cli"


class OutputFormat(Enum):
    table = "table"
    json = "json"


def save_config(config_values: Dict) -> confuse.Configuration:
    config = read_config()

    if config.exists():
        config.clear()

    config.add(config_values)
    with open(config.user_config_path(), "w") as file:
        file.seek(0)
        file.write(config.dump())
        file.truncate()

    return config


def read_config() -> confuse.Configuration:
    return confuse.Configuration(APP_NAME)


def exit_cli(message: str, status_code: int) -> None:
    status_symbol = "✅" if status_code == 0 else "❌"
    typer.echo(f"{status_symbol}  {message}", err=True)
    sys.exit(status_code)


def show_progress():
    sys.stderr.write(".")
    sys.stderr.flush()
