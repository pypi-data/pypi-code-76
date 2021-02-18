import click
from sym.cli.decorators import setup_segment, setup_sentry
from sym.cli.helpers.sym_group import SymGroup
from sym.cli.helpers.updater import SymUpdater

from sym.flow.cli.commands.debug import debug_commands
from sym.flow.cli.commands.integrations import integration_commands
from sym.flow.cli.commands.login import login
from sym.flow.cli.commands.update import update
from sym.flow.cli.commands.version import version

from ..helpers.constants import (
    DEFAULT_API_URL,
    DEFAULT_AUTH_URL,
    SegmentWriteKey,
    SentryDSN,
)
from ..helpers.global_options import GlobalOptions
from ..version import __version__


@click.group(
    name="symflow", cls=SymGroup, context_settings={"help_option_names": ["-h", "--help"]}
)
@click.option(
    "--debug", is_flag=True, help="enable verbose debugging", envvar="SYM_DEBUG"
)
@click.option(
    "--api-url",
    default=DEFAULT_API_URL,
    help="set the Sym API URL",
    envvar="SYM_API_URL",
)
@click.option(
    "--auth-url",
    default=DEFAULT_AUTH_URL,
    help="set the Sym auth url",
    envvar="SYM_AUTH_URL",
)
@click.make_pass_decorator(GlobalOptions, ensure=True)
@setup_segment(write_key=SegmentWriteKey)
@setup_sentry(dsn=SentryDSN, release=f"sym-flow-cli@{__version__}")
def symflow(options: GlobalOptions, auth_url: str, api_url: str, debug: bool) -> None:
    """
    Author Sym Flows

    Use this CLI to author Sym Flows.
    https://docs.symops.com/docs/support
    """

    options.debug = debug
    options.api_url = api_url
    options.auth_url = auth_url
    options.dprint(auth_url=auth_url, api_url=api_url)

    SymUpdater(debug=debug).auto_update()


symflow.add_command(version)
symflow.add_command(update)
symflow.add_command(login)
symflow.add_command(integration_commands)
symflow.add_command(debug_commands)
