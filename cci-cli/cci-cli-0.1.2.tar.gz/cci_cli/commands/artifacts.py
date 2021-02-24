from pathlib import Path, PurePath
from typing import Optional, List

import typer
from tabulate import tabulate

from cci_cli.circle.api import CircleCI

artifacts_app = typer.Typer()
ARTIFACTS_TABLE_HEADERS = ["Job", "Job Number", "Node Index", "Path", "URL"]


@artifacts_app.command(help="List artifacts of a specific pipeline id")
def list(
    pipeline_id: str,
    artifact_patterns: List[str] = typer.Argument(None),
):
    cci = CircleCI()
    artifacts = cci.read_pipeline_artifacts(
        pipeline_id, *(artifact_patterns or tuple())
    )
    typer.echo(tabulate(artifacts, headers=ARTIFACTS_TABLE_HEADERS))


@artifacts_app.command(help="Download the artifacts of a specific pipeline id")
def download(
    pipeline_id: str,
    output_path: Path,
    artifact_patterns: List[str] = typer.Argument(None),
    trim_prefix: Optional[str] = None,
    overwrite: bool = False,
    verbose: bool = False,
):
    cci = CircleCI()
    artifacts = cci.read_pipeline_artifacts(
        pipeline_id, *(artifact_patterns or tuple())
    )
    if verbose:
        typer.echo(tabulate(artifacts, headers=ARTIFACTS_TABLE_HEADERS))

    for artifact in artifacts:
        job_name, job_number, node_index, path, url = artifact
        typer.echo(
            f"Downloading artifact {path} of job ({job_number}/{node_index}) {job_name}..."
        )

        path = path.lstrip("~/")
        if trim_prefix is not None:
            trim_prefix = trim_prefix.lstrip("~/")
            if path.startswith(trim_prefix):
                prefix_len = len(trim_prefix)
                path = path[prefix_len:].lstrip("~/")

        path = PurePath(path)
        full_path = output_path.joinpath(f"job-{job_number}-{node_index}", path)

        if full_path.exists() and not overwrite:
            if verbose:
                typer.echo(f"Skipped {full_path}. Already exists.")
                typer.echo()
            continue

        if not full_path.parent.is_dir() and verbose:
            typer.echo(f"Creating parent directory {full_path.parent}/...")
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with full_path.open("wb") as output_file:
            if verbose:
                typer.echo(f"Writing to {full_path}...")
            for current_offset, total_bytes in cci.download_request(url, output_file):
                if verbose:
                    typer.echo(f"Progress: {current_offset}/{total_bytes} bytes")

        if verbose:
            typer.echo("Download done.")
            typer.echo()
