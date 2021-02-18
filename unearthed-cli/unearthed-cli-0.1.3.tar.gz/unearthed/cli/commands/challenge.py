"""Unearthed Challenge command."""
import logging

import click
import requests
from unearthed.cli.auth import auth_handler
from unearthed.cli.config import LAMBDA_URL
from unearthed.cli.auth import authorize

from unearthed.core.models.challenge import Challenge

logger = logging.getLogger(__name__)


@click.group()
def challenge():
    """Inspect Unearthed challenges."""
    pass


@challenge.command("ls")
@authorize
def ls():
    """List challenges."""
    for challenge in Challenge.allFromApi():
        print(
            f"{challenge['slug']}: {challenge['name']} "
            f"({challenge['innovatorPlatformRef']})"
        )
