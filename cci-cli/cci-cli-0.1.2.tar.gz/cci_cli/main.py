import os

import typer

from cci_cli.commands.artifacts import artifacts_app
from cci_cli.commands.config import config_app
from cci_cli.commands.pipelines import pipelines_app
from cci_cli.commands.workflows import workflows_app

app = typer.Typer()
app.add_typer(artifacts_app, name="artifacts", help="Manage pipeline artifacts")
app.add_typer(pipelines_app, name="pipelines", help="Manage pipelines")
app.add_typer(config_app, name="config", help="Configure the CCI CLI")
app.add_typer(workflows_app, name="workflows", help="Manage workflows")


@app.command(help="Display current CLI version")
def version():
    version_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "VERSION")
    )
    with open(version_file_path) as f:
        v = f.readline()
    typer.echo(f"CLI Version: {v}")
    raise typer.Exit()
