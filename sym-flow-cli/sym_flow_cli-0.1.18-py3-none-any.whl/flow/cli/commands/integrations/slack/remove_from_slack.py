import webbrowser

import click
import requests
from sym.cli.errors import CliError

from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.sym_api_client import SymAPIClient


@click.command(name="remove", short_help="Remove Sym app from Slack")
@click.option(
    "-n",
    "--name",
    required=True,
    prompt="Slack Integration Name",
    help="Name used to identify your Sym Slack Integration",
)
@click.make_pass_decorator(GlobalOptions, ensure=True)
def remove_from_slack(options: GlobalOptions, name: str) -> None:
    """Remove the Sym Slack App from your Slack workspace.

    To see a list of existing Sym Integrations, run `symflow integrations list`.
    """

    slack_uninstall(api_url=options.api_url, integration_name=name)
    click.echo(
        "Uninstall successful! The Sym app has been removed from your Slack workspace."
    )


def slack_uninstall(api_url: str, integration_name: str):
    api_client = SymAPIClient(url=api_url)
    api_client.uninstall_slack(integration_name=integration_name)
