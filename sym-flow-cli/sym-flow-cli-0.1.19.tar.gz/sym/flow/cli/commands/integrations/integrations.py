import click
from sym.cli.helpers.sym_group import SymGroup

from sym.flow.cli.helpers.global_options import GlobalOptions

from .integrations_list import integrations_list
from .slack import slack_commands


@click.group(cls=SymGroup, short_help="Perform operations on Sym Integrations")
@click.make_pass_decorator(GlobalOptions, ensure=True)
def integrations(options: GlobalOptions) -> None:
    """Sym Flow CLI commands for operations on Integrations.

    Sym Integrations can be managed via Terraform. For more details,
    see https://docs.symops.com/docs/integrations
    """


integrations.add_command(integrations_list)
integrations.add_command(slack_commands)
