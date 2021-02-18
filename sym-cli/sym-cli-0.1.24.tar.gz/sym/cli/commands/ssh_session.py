import click

from sym.cli.helpers.global_options import GlobalOptions

from ..actions.action_registry import ActionRegistry
from ..data.request_data import RequestData
from ..data.target_options import TargetOptions
from ..decorators import loses_interactivity, require_login, skip_analytics
from ..helpers.global_options import GlobalOptions
from ..helpers.options import resource_argument
from .sym import sym


@sym.command(hidden=True, short_help="Starts a SSH session over SSM")
@resource_argument
@click.option("--instance", help="Instance ID to connect to", required=True)
@click.option("--port", default=22, type=int, show_default=True)
@click.make_pass_decorator(GlobalOptions)
@skip_analytics
@require_login
@loses_interactivity
def ssh_session(options: GlobalOptions, resource: str, instance: str, port: int):
    target_options = TargetOptions(host=instance, port=port)
    request_data = RequestData(
        action="ssh_session",
        resource=resource,
        global_options=options,
        target_options=target_options,
    )

    ActionRegistry.execute(request_data)
