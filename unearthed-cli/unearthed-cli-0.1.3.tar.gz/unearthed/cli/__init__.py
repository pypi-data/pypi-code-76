"""Unearthed CLI entry point."""
import logging

import click
import unearthed.logs
from unearthed.cli.errors import check_version_and_warn
from pkg_resources import get_distribution

from .commands.auth import auth, login, logout
from .commands.build import build
from .commands.challenge import challenge
from .commands.new import new
from .commands.predict import predict
from .commands.preprocess import preprocess
from .commands.reset import reset
from .commands.submit import submit
from .commands.tracker import tracker
from .commands.train import train
from .commands.score import score

# check the version of the Unearthed CLI
check_version_and_warn()

logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version=get_distribution("unearthed-cli").version)
def main():
    """Unearthed CLI."""
    pass


# add commands to the CLI command root
# logger.debug("adding commands")
main.add_command(login)
main.add_command(logout)
main.add_command(new)
main.add_command(build)
main.add_command(submit)
main.add_command(tracker)
main.add_command(reset)
main.add_command(challenge)
main.add_command(auth)
main.add_command(preprocess)
main.add_command(train)
main.add_command(predict)
main.add_command(score)
