#!/usr/bin/env python
import click
import os.path
import sys
from functools import partial

from crc_manager.util import make_logger, verbose_opt


logger = make_logger()


@click.group()
@verbose_opt
@click.version_option()
def main(verbose):
    """
    CodeReady Containers Manager

    Manage the crc binary and virtual machine.
    """
    logger = make_logger(verbose)
    logger.debug(sys.argv)
    logger.debug(f'verbose: {verbose}')


# Show default values for all subcommands
click.option = partial(click.option, show_default=True)


@main.command()
@verbose_opt
@click.option('-d', '--directory', default=os.path.expanduser('~/.crc'),
              help='The directory into which to unpack the crc installer')
@click.option('-p', '--path', default=os.path.expanduser('~/.local/bin'),
              help='The directory in your $PATH to symlink crc into')
@click.option(
    '-m', '--mirror', help='The crc mirror to download from',
    default='https://mirror.openshift.com/pub/openshift-v4/clients/crc/latest'
)
def update(verbose, directory, path, mirror):
    """Updates the crc binary, validating sums"""
    logger = make_logger(verbose)
    logger.debug(f'verbose: {verbose}')
    logger.debug(f'directory: {directory}')
    logger.debug(f'path: {path}')
    logger.debug(f'mirror: {mirror}')

    from crc_manager.update import crc_update
    version = crc_update(directory=directory, path=path, mirror=mirror)

    if path in os.getenv('PATH').split(':'):
        print(f'crc version {version} is in your path as `crc`')
    else:
        print(f'crc version {version} is available at {path}/crc')
