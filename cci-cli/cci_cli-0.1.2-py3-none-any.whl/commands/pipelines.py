from contextlib import suppress
from itertools import starmap
from json import dumps, loads, JSONDecodeError
import re
import warnings
from typing import Optional, List

import typer
from tabulate import tabulate

from cci_cli.circle.api import CircleCI
from cci_cli.common import utils

pipelines_app = typer.Typer()
PIPELINES_TABLE_HEADERS = [
    "Pipeline ID",
    "Created at",
    "State",
    "Trigger",
    "Actor",
    "Branch",
    "URL",
]
PIPELINES_JSON_HEADERS = ["id", "created", "state", "trigger", "actor", "branch", "url"]


@pipelines_app.command(help="List pipelines for a specific project name")
def list(
    project_name: str,
    branch: Optional[str] = typer.Argument(None),
    after_pipeline_id: Optional[str] = typer.Option(
        "--after",
        "--after-pipeline-id",
        help="String pipeline id. "
        "Only list pipelines that were created after this one. "
        "Used in fleet to check if the current pipeline needs to be canceled.",
    ),
    format: utils.OutputFormat = typer.Option("table"),
):
    cci = CircleCI()
    pipelines = cci.list_pipelines(project_name, branch, after_pipeline_id)
    if format == utils.OutputFormat.json:
        pipeline_json = [
            dict(zip(PIPELINES_JSON_HEADERS, pipeline)) for pipeline in pipelines
        ]
        out = dumps(pipeline_json)
    else:
        out = tabulate(pipelines, headers=PIPELINES_TABLE_HEADERS)
    typer.echo(out)


@pipelines_app.command(help="Trigger a pipeline for a specific project and branch")
def trigger(
    project_name: str,
    params_list: List[str] = typer.Argument(
        None,
        metavar="[PARAM_KEY=VALUE ...]",
        help=(
            "Parameters to set on the pipeline to trigger. "
            "PARAM_KEY should be a valid env-var-like name. "
            "VALUE cannot contain an equal sign."
            "If VALUE is valid json, it is parsed & sent as the appropriate type, "
            "otherwise it will be handled like a string"
        ),
    ),
    branch: Optional[str] = typer.Option(
        "",
        "--branch",
        "-b",
        help=(
            "Branch to trigger the pipeline on (instead of tag). "
            "By default, the main branch as configured on GitHub/Bitbucket."
        ),
    ),
    tag: Optional[str] = typer.Option(
        "", "--tag", "-t", help="Tag to trigger the pipeline on (instead of branch)."
    ),
    params: Optional[str] = typer.Option(
        None, "--params", "-p", help="Deprecated, use [PARAM_KEY=VALUE ...] instead."
    ),
    wait_for_result: Optional[bool] = typer.Option(False),
    timeout: Optional[int] = typer.Option(15, "--timeout", "-t"),
):
    """
    Trigger a pipeline for the specified projects.

    --branch and --tag are mutually exclusive.
    If neither is specified, a pipeline on the HEAD of the main branch is triggered.
    """
    _validate_options(branch, tag)
    params = _build_params_dict(params, params_list)

    cci = CircleCI()
    trigger_response = cci.trigger(
        project_name=project_name, branch=branch, tag=tag, parameters=params
    )
    pipeline_id = trigger_response.get("id")
    typer.echo(
        f"{trigger_response['created_at']}: Pipeline with ID {trigger_response['id']} was created.",
        err=True,
    )

    typer.echo("Waiting for workflows to start...", err=True)
    workflows = cci.wait_for_workflows_creation(pipeline_id, timeout=timeout)
    typer.echo("You can check your pipeline here:", err=True)
    for workflow in workflows:
        url = cci.get_workflow_url(workflow)
        typer.echo(f"    {url}", err=True)

    if wait_for_result:
        cci.wait_for_workflows_completion(pipeline_id, timeout=timeout)


@pipelines_app.command(help="Get all workflows for a specific pipeline id")
def get_workflows(
    pipeline_id: str,
    format: utils.OutputFormat = typer.Option("table"),
):
    cci = CircleCI()
    workflows_json = cci.get_workflows(pipeline_id)
    if format == utils.OutputFormat.json:
        out = dumps(workflows_json)
    else:
        workflows = [
            (workflow["name"], workflow["id"], workflow["status"])
            for workflow in workflows_json
        ]
        out = tabulate(workflows, headers=("Name", "ID", "status"))
    typer.echo(out)


@pipelines_app.command(help="List newer workflows")
def newer_workflows(
    project_name: str,
    after_pipeline_id: str,
    branch: Optional[str] = typer.Argument(None),
    format: utils.OutputFormat = typer.Option("table"),
):
    cci = CircleCI()
    newer_pipelines = cci.list_pipelines(project_name, branch, after_pipeline_id)
    workflows_json = []
    for pipeline_id, *_ in newer_pipelines:
        workflows = cci.get_workflows(pipeline_id)
        for workflow in workflows:
            workflows_json.append(workflow)

    if format == utils.OutputFormat.json:
        out = dumps(workflows_json)
    else:
        workflows = [
            (
                workflow["pipeline_id"],
                workflow["name"],
                workflow["id"],
                workflow["status"],
            )
            for workflow in workflows_json
        ]
        out = tabulate(workflows, headers=("Pipeline", "Name", "ID", "status"))
    typer.echo(out)


def _validate_params(params: str):
    pattern = re.compile(r"(?:(?:^|,)[\d\w\-_]+=[\d\w\-\._+]+)+")
    if pattern.fullmatch(params):
        message = "Use trigger [PARAM_KEY=VALUE ...] instead of trigger --params KEY=VALUE,..."
        warnings.warn(DeprecationWarning(message))
        typer.echo("DeprecationWarning: --params is deprecated. " + message, err=True)
        return
    utils.exit_cli(
        message="Error: Note that parameters must be passed like 'KEY_1=VAL-UE_1,key-2=value.2'\n"
        "Keys may contain: upper and lowercase characters, digits, '_', and '-'\n"
        "Values may contain: upper and lowercase characters, digits, '_', '-', and '.'",
        status_code=1,
    )


def _validate_param_new_style(param: str):
    pattern = re.compile(r"[\d\w\-_]+=[^=]+")
    if pattern.fullmatch(param):
        return
    utils.exit_cli(
        message="Error: Note that parameters must be passed like 'KEY_1=VAL-UE_1 key-2=value.2'\n"
        "Keys may contain: upper and lowercase characters, digits, '_', and '-'\n"
        "Values may contain: anything but '='",
        status_code=1,
    )


def _build_params_dict(params_old_style, params_new_style):
    parameters = {}

    # Add old-style first after validation (if specified)
    if params_old_style is not None:
        _validate_params(params_old_style)
        parameters.update(
            key_value.split("=", maxsplit=1)
            for key_value in params_old_style.split(",")
        )

    # New-style will take precedence (if specified)
    if params_new_style is not None:
        for param_item in params_new_style:
            _validate_param_new_style(param_item)
        parameters.update(
            key_value.split("=", maxsplit=1) for key_value in params_new_style
        )

    parameters = dict(starmap(_preprocess_param, parameters.items()))

    return parameters


def _preprocess_param(key, value):
    with suppress(JSONDecodeError):
        parsed_value = loads(value)
        if isinstance(parsed_value, (str, int, float, bool)):
            value = parsed_value
    return (key, value)


def _validate_options(branch, tag):
    if bool(branch and tag):
        utils.exit_cli(
            message="Error: Note that branch and tag are mutually exclusive "
            "and may not be used at the same time.",
            status_code=1,
        )
