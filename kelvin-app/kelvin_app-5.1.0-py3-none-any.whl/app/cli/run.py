"""Run Applications."""

from __future__ import annotations

from typing import Optional

import click
import structlog
from click.exceptions import Exit

from ..client.run import InterfaceType, LogLevel, run_app
from ..logs import configure_logs
from ..server import DevServer
from .main import main

logger = structlog.get_logger(__name__)


@main.group()
def run() -> None:
    """Run Applications and Servers."""


@run.command()
@click.option(
    "--interface-type",
    "-i",
    type=click.Choice([*InterfaceType]),
    required=False,
    help="Interface type",
)
@click.option("--sub-url", "-s", type=click.STRING, required=False, help="Subscription URL")
@click.option("--pub-url", "-p", type=click.STRING, required=False, help="Publish URL")
@click.option("--configuration", "-c", type=click.STRING, required=False, help="App configuration")
@click.option(
    "--log-level",
    "-l",
    type=click.Choice([x.name for x in LogLevel]),
    default=None,
    callback=lambda _, __, x: LogLevel[x] if x is not None else None,
    help="Logging level",
)
@click.option("--max-steps", "-m", type=click.INT, required=False, help="Maximum number of steps")
@click.argument("entry_point", nargs=1, type=click.STRING)
def app(
    interface_type: Optional[InterfaceType],
    sub_url: Optional[str],
    pub_url: Optional[str],
    configuration: Optional[str],
    log_level: Optional[LogLevel],
    max_steps: Optional[int],
    entry_point: str,
) -> None:
    """Run Kelvin Applications."""

    if log_level is not None:
        configure_logs(default_level=log_level)

    try:
        run_app(entry_point, interface_type, sub_url, pub_url, configuration, max_steps, log_level)
    except Exception as e:  # pragma: no cover
        logger.exception("Failed")
        click.echo(f"Unable to run app: {e}", err=True)
        raise Exit(1)


@run.command()
@click.option(
    "--loop/--no-loop",
    default=True,
    help="Option to only inject data from input CSV once, without looping",
)
@click.option(
    "--verbose/--silent",
    "-v/-s",
    default=True,
    help="Option to print messages when injected",
)
@click.option(
    "--pub-url",
    default="tcp://127.0.0.1:10411",
    help="Which port to publish the Data. Default: tcp://127.0.0.1:10413",
)
@click.option(
    "--extract-path",
    default="",
    help="Give a relative location to extract data from application. Data will not be extracted unless path provided",
)
@click.option(
    "--extract-type",
    default="parquet",
    type=click.Choice(["parquet", "csv"], case_sensitive=False),
    help="Options: 'parquet' or 'csv'",
)
@click.option(
    "--sub-url",
    default="tcp://127.0.0.1:21813",
    help="Which port to listen for app data. Default: tcp://127.0.0.1:21813",
)
@click.option(
    "--topic",
    default="",
    help="Topic prefix to subscribe to",
)
@click.option(
    "--frequency",
    default=1.0,
    type=float,
    help="Speed at which to cycle through injection data. Default 1 per second",
)
@click.argument("data_path", nargs=1, type=click.STRING)
def server(
    data_path: str,
    pub_url: str,
    loop: bool,
    verbose: bool,
    extract_path: str,
    extract_type: str,
    sub_url: str,
    topic: str,
    frequency: float,
) -> None:
    """Run Server and inject data from CSV at DATA_PATH."""
    try:
        ds = DevServer(
            data_path,
            pub_url,
            loop,
            verbose,
            extract_path,
            extract_type,
            sub_url,
            topic,
            frequency,
        )
        ds.run()
    except Exception as e:
        click.echo(f"Unable to run server: {e}", err=True)
        raise Exit(1)
