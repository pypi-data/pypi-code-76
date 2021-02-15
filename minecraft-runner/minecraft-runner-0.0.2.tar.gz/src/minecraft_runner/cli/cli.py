"""Minecraft Runner - A python script for working with servers.

This module is for providing the main command line interface functions.
"""

import click
import sys

from ..util import get_logger
from .util import container_exists, verbose_opt, disclaimer

from ..manage import containers

logger = get_logger()


@click.group(epilog=disclaimer)
@verbose_opt
@click.version_option()
def main(verbose):
    """Manage and interact with Minecraft server containers.

    This client is designed to interact with special container images
    specifically designed for its use. It is not designed to work with generic
    Minecraft server implementations.
    """
    logger = get_logger(verbose)
    logger.debug(sys.argv)
    logger.debug(f'verbose: {verbose}')


@main.command()
@verbose_opt
@click.option('-a', '--all', 'all_containers', is_flag=True,
              help="List all configured containers, running or otherwise.")
def ls(verbose, all_containers):
    """List all configured containers currently running."""
    logger = get_logger(verbose)
    logger.debug(f'verbose: {verbose}')
    logger.debug(f'all: {all_containers}')

    for name in containers:
        if all_containers:
            click.echo(name)
        else:
            for line in containers[name].show():
                if line.endswith(f' {name}'):
                    click.echo(name)


@main.command()
@verbose_opt
@click.argument('name', callback=container_exists)
def show(verbose, name):
    """Show the details of a configured container.

    NAME is the name of the configured container image to show.
    """
    logger = get_logger(verbose)
    logger.debug(f'verbose: {verbose}')
    logger.debug(f'name: {name}')

    [click.echo(line) for line in containers[name].show()]
