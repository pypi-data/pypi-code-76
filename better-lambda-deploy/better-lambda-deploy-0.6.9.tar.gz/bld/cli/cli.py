import click
from .deploy import commands as deploy
from .start_api import commands as start_api
from .invoke import commands as invoke


@click.group()
def entry_point():
    pass


entry_point.add_command(deploy.deploy)
entry_point.add_command(start_api.start_api)
entry_point.add_command(invoke.invoke)


if __name__ == "__main__":
    entry_point()
