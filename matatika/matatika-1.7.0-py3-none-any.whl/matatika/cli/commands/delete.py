"""CLI 'delete' command and subcommands"""

import click
from matatika.cli.utility import Resolver
from matatika.types import Resource
from .root import matatika


@matatika.group('delete', short_help='Delete a resource')
@click.pass_context
@click.option("--bypass-confirm", is_flag=True, help="Bypass delete confirmation")
def delete(ctx, bypass_confirm):
    """Delete a resource"""

    ctx.obj['bypass_confirm'] = bypass_confirm


@delete.command('workspace', short_help='Delete a workspace')
@click.pass_context
@click.argument("workspace-id", type=click.UUID)
def delete_workspace(ctx, workspace_id):
    """Delete a workspace"""

    delete_confirmed = ctx.obj['bypass_confirm']

    client = Resolver(ctx).client(workspace_id=None)

    if not delete_confirmed:
        confirmation_message = "This action cannot be undone. Do you want to continue? [y/N]"
        delete_confirmed = click.confirm(
            text=_warning(confirmation_message),
            prompt_suffix=_warning(": "),
            show_default=False)

    if delete_confirmed:
        client.delete_resource(Resource.WORKSPACE, workspace_id)
        click.secho(
            f"Successfully deleted workspace {workspace_id}", fg='green')


@delete.command('dataset', short_help='Delete a dataset')
@click.pass_context
@click.argument("dataset-id", type=click.UUID)
def delete_dataset(ctx, dataset_id):
    """Delete a dataset"""

    delete_confirmed = ctx.obj['bypass_confirm']

    client = Resolver(ctx).client(workspace_id=None)

    if not delete_confirmed:
        confirmation_message = "This action cannot be undone. Do you want to continue? [y/N]"
        delete_confirmed = click.confirm(
            text=_warning(confirmation_message),
            prompt_suffix=_warning(": "),
            show_default=False)

    if delete_confirmed:
        client.delete_resource(Resource.DATASET, dataset_id)
        click.secho(f"Successfully deleted dataset {dataset_id}", fg='green')


def _warning(text: str) -> str:

    return click.style(text, fg='yellow')
