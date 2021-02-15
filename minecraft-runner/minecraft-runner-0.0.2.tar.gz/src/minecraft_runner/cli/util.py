"""Minecraft Runner - A python script for working with servers.

This module provides some basic CLI utilities, like common options.
"""

import click
from ..manage import containers


def verbose_opt(func):
    """Wrap the function in a click.option for verbosity."""
    return click.option(
        "-v", "--verbose", count=True,
        help="Increase verbosity (specify multiple times for more)."
    )(func)


def container_exists(ctx, param, value: str = None) -> str:
    """Ensure that the container name is in the list of configured servers."""
    if value in containers.keys():
        return value
    raise click.BadParameter("The name provided isn't a defined container!")


disclaimer = """
NOTE: This project is wholely unaffiliated with FeedTheBeast, Minecraft,
Mojang, and Microsoft. It is an independent release to make management of local
servers simpler.
"""
