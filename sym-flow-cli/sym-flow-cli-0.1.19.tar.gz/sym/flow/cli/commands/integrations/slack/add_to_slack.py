import webbrowser

import click

from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.sym_api_client import SymAPIClient


@click.command(name="add", short_help="Add Sym app to Slack")
@click.option(
    "-n",
    "--name",
    required=True,
    prompt="Slack Integration Name",
    help="Name used to identify your Sym Slack Integration",
)
@click.make_pass_decorator(GlobalOptions, ensure=True)
def add_to_slack(options: GlobalOptions, name: str) -> None:
    """Install the Sym Slack App into your Slack workspace. Will open a
    browser window to confirm the installation.

    Run this command after performing a terraform apply to create your Sym Integrations.
    To see a list of existing Sym Integrations, run `symflow integrations list`.
    """

    initialize_slack_install(api_url=options.api_url, integration_name=name)


def initialize_slack_install(api_url: str, integration_name: str):
    api_client = SymAPIClient(url=api_url)
    url, _ = api_client.get_slack_install_url(integration_name=integration_name)
    webbrowser.open(url)
