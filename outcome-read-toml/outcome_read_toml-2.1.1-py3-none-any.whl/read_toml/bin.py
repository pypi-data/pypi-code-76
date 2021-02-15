#! /usr/bin/env python3

"""A utility to read values from TOML files."""

import sys
from pathlib import Path
from typing import IO, Optional, Union

import click
from outcome.read_toml.lib import read, read_from_file  # noqa: WPS347


@click.command()
@click.option('--path', help='The path to the TOML file', required=True, type=click.File('r'))
@click.option('--key', help='The path to read from the TOML file', required=True)
@click.option('--default', help='The value to provide if the key is missing', required=False)
@click.option('--check-only', help='If present, only checks if the key is present in the TOML file', is_flag=True, default=False)
def read_toml_cli(path: IO[str], key: str, check_only: bool, default: Optional[str] = None):
    """Read the value specified by the path from a TOML file.

    The path parameter should be a '.' separated sequences of keys
    that correspond to a path in the TOML structure.

    Example TOML file:

    ---
    title = "My TOML file"

    [info]
    version = "1.0.1"

    [tools.poetry]
    version = "1.1.2"
    files = ['a.py', 'b.py']
    ---

    Read standard keys:

    read_toml.py --path my_file.toml --key title -> "My TOML file"
    read_toml.py --path my_file.toml --key info.version -> "1.0.1"

    Read arrays:

    read_toml.py --path my_file.toml --key tools.poetry.files -> "a.py b.py"

    Read non-leaf keys:

    read_toml.py --path my_file.toml --key tools -> #ERROR

    Check if key exists:

    read_toml.py --path my_file.toml --key tools --check-only -> 1 if key exists
    read_toml.py --path my_file.toml --key tools --check-only -> 0 if key does not exist

    Args:
        path (str): The path to the file.
        key (str): The path to the key to read.
        check_only (bool): If True, only checks if key exists
        default (str, optional): If the key doesn't exist, print this value.
    """
    click.echo(read_toml(path, key, check_only, default))


def read_toml(
    path: Union[IO[str], str, Path], key: str, check_only: bool = False, default: Optional[str] = None,
):
    try:
        if isinstance(path, (str, Path)):
            value = read_from_file(path, key)
        else:
            value = read(path, key)

        if check_only:
            value = '1'
    except KeyError as ex:
        if check_only:
            value = '0'
        elif default is not None:
            value = default
        else:
            fail(str(ex))

    return value  # noqa: R504


def fail(key: str):  # pragma: no cover
    click.echo(f'Invalid key: {key}', err=True)
    sys.exit(-1)


def main():
    read_toml_cli()
