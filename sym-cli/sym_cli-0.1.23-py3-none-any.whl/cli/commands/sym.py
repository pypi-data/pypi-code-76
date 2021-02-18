from typing import Optional

import click

from sym.cli.helpers.sym_group import SymGroup

from ..decorators import setup_segment, setup_sentry
from ..helpers.constants import SegmentWriteKey, SentryDSN
from ..helpers.envvar_option import EnvvarOption
from ..helpers.global_options import GlobalOptions
from ..helpers.options import resource_option
from ..helpers.sym_group import SymGroup
from ..helpers.updater import SymUpdater
from ..saml_clients.chooser import SAMLClientName, choose_saml_client, option_values
from ..version import __version__


@click.group(
    name="sym", cls=SymGroup, context_settings={"help_option_names": ["-h", "--help"]}
)
@click.option(
    "--saml-client",
    "saml_client_name",
    default="auto",
    type=click.Choice(option_values()),
    help="The SAML client type to use",
    envvar="SYM_SAML_CLIENT",
    cls=EnvvarOption,
)
@click.option(
    "--debug", is_flag=True, help="Enable verbose debugging", envvar="SYM_DEBUG"
)
@click.option("--aws-region", envvar="AWS_REGION", hidden=True)
@click.option(
    "--log-dir",
    type=click.Path(dir_okay=True, file_okay=False),
    hidden=True,
    envvar="SYM_LOG_DIR",
)
@click.option(
    "--session-length",
    type=click.INT,
    help="The length of the session requested from STS.",
    envvar="SYM_SESSION_LENGTH",
)
@click.make_pass_decorator(GlobalOptions, ensure=True)
@resource_option
@setup_segment(write_key=SegmentWriteKey)
@setup_sentry(dsn=SentryDSN, release=f"sym-cli@{__version__}")
def sym(
    options: GlobalOptions,
    saml_client_name: SAMLClientName,
    debug: bool,
    resource: str,
    aws_region: str,
    log_dir: Optional[str],
    session_length: Optional[int],
) -> None:
    """
    Access resources managed by Sym Flows.

    Use this CLI to interact with resources you've received access to with Sym.
    https://docs.symops.com/docs/setup-sym-cli
    """
    options.saml_client_type = choose_saml_client(saml_client_name, none_ok=True)
    options.debug = debug
    options.log_dir = log_dir
    options.aws_region = aws_region
    options.session_length = session_length

    SymUpdater(debug=debug).auto_update()
