from json import dumps

from requests.exceptions import HTTPError

import typer
from tabulate import tabulate

from cci_cli.circle.api import CircleCI
from cci_cli.circle.exceptions import CircleCIException
from cci_cli.common import utils

workflows_app = typer.Typer()


@workflows_app.command(help="get information about a workflow")
def get(workflow_id: str, format: utils.OutputFormat = typer.Option("table")):
    cci = CircleCI()
    wf_json = cci.get_workflow(workflow_id)
    if format == utils.OutputFormat.json:
        out = dumps(wf_json)
    else:
        out = tabulate(
            (wf_json["name"], wf_json["id"], wf_json["status"]),
            headers=("Name", "ID", "status"),
        )
    typer.echo(out)


@workflows_app.command(help="Approve a specific workflow by id")
def approve(workflow_id: str):
    cci = CircleCI()
    try:
        cci.approve_on_hold_jobs(workflow_id)
    except CircleCIException as ex:
        utils.exit_cli(
            message=str(ex),
            status_code=ex.status_code,
        )


@workflows_app.command(help="Cancel a specific workflow by id")
def cancel(workflow_id: str):
    cci = CircleCI()
    try:
        cci.cancel_workflow(workflow_id)
    except HTTPError as e:
        utils.exit_cli(
            message=e,
            status_code=1,
        )


@workflows_app.command()
def rerun(workflow_id: str):
    cci = CircleCI()
    try:
        cci.rerun_workflow(workflow_id)
    except HTTPError as e:
        utils.exit_cli(
            message=e,
            status_code=1,
        )
