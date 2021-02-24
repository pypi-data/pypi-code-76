import os
from typing import Optional

import typer

from cci_cli.common import utils

config_app = typer.Typer()


def _evaluate_vcs(value: str):
    if value not in ["gh", "bb"]:
        raise typer.BadParameter("vcs can only be one of {'gh', 'bb'}.")
    return value


@config_app.command(help="Configure the CCI CLI")
def setup(
    vcs: Optional[str] = typer.Option(
        None,
        callback=_evaluate_vcs,
        prompt="Which VCS are you using (Github/BitBucket)",
    ),
    org: Optional[str] = typer.Option(
        None, prompt="Please input your organization/username"
    ),
    token: Optional[str] = typer.Option(
        None, prompt="Please input your CircleCI token"
    ),
):
    configuration = utils.save_config(
        {"vcs": vcs, "organization": org, "circle_token": token}
    )

    filename = os.path.basename(configuration.user_config_path())
    utils.exit_cli(message=f"Configuration File created at {filename}", status_code=0)


@config_app.command(help="Display the path to the current configuration file")
def locate():
    configuration = utils.read_config()
    typer.echo(configuration.user_config_path())


@config_app.command(help="Display the current configuration")
def show():
    configuration = utils.read_config()
    typer.echo(configuration.dump())
