from pathlib import Path

import click

from hycli import __version__


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f"Version {__version__}")
    ctx.exit()


def find_skippable_files(ctx, param, value):
    # Todo: parse xlsx/csv and concat the values from input which are not found here.
    value = Path(value).resolve()
    ctx.obj = {"skip_files": value.rglob("*.json") if ctx.params["skip"] else []}

    return value


def parse_arguments(ctx, param, values):
    return {v.split(":")[0].strip(): v.split(":")[1].strip() for v in values}
