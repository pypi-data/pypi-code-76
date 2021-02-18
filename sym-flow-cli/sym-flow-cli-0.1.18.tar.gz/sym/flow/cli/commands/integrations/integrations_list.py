from typing import List

import click
from tabulate import tabulate

from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.sym_api_client import SymAPIClient
from sym.flow.cli.helpers.sym_api_service import SymAPIService


@click.command(name="list", short_help="View all integrations")
@click.make_pass_decorator(GlobalOptions, ensure=True)
def integrations_list(options: GlobalOptions) -> None:
    """View all Sym Integrations currently set up for your organization.

    Sym Integrations can be added or removed via Terraform. For more details,
    see https://docs.symops.com/docs/integrations
    """

    click.echo(get_integration_data(options.api_url))


def get_integration_data(api_url: str) -> str:
    api_service = SymAPIService(api_client=SymAPIClient(url=api_url))
    return tabulate(
        api_service.get_integration_table_data(), headers=["Name", "Type", "Last Updated"]
    )
