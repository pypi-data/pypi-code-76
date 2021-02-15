"""Main command."""

import click

from kelvin.icd.cli.main import Group


@click.group(cls=Group)
def main() -> None:
    """Kelvin Core Client CLI."""
