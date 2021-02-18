import click
from sym.cli.helpers.sym_group import SymGroup

from sym.flow.cli.helpers.global_options import GlobalOptions

from .add_to_slack import add_to_slack
from .remove_from_slack import remove_from_slack


@click.group(cls=SymGroup, short_help="Perform operations on Sym Slack Integrations")
@click.make_pass_decorator(GlobalOptions, ensure=True)
def slack(options: GlobalOptions) -> None:
    """Sym Flow CLI commands for operations on Slack Integrations.

    Sym Integrations can be managed via Terraform. For more details,
    see https://docs.symops.com/docs/integrations
    """


slack.add_command(add_to_slack)
slack.add_command(remove_from_slack)
