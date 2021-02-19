"""CLI 'list' command and subcommands"""

import click
from matatika.cli.utility import create_table, Resolver
from matatika.types import Resource
from .root import matatika


@matatika.group('list', short_help='List all available resources')
def list_():
    """Display a list of all available resources of a specified type"""


@list_.command('workspaces', short_help='List all available workspaces')
@click.pass_context
def list_workspaces(ctx):
    """Display a list of all available workspaces"""

    client = Resolver(ctx).client(workspace_id=None)
    workspaces = client.list_resources(Resource.WORKSPACE)

    ids = ['WORKSPACE ID']
    names = ['NAME']

    for workspace in workspaces:
        ids.append(workspace['id'])
        names.append(workspace['name'])

    table = create_table(ids, names)
    click.echo(table)
    click.echo(f"\nTotal workspaces: {len(workspaces)}")


@list_.command('datasets', short_help='List all available datasets')
@click.pass_context
@click.option('--workspace-id', '-w', type=click.UUID, help='Workspace ID')
def list_datasets(ctx, workspace_id):
    """Display a list of all available datasets"""

    ctx.obj['workspace_id'] = workspace_id
    client = Resolver(ctx).client()
    datasets = client.list_resources(Resource.DATASET)

    ids = ['DATASET ID']
    aliases = ['ALIAS']
    titles = ['TITLE']

    for dataset in datasets:
        ids.append(dataset['id'])
        aliases.append(dataset['alias'])
        titles.append(dataset['title'])

    table = create_table(ids, aliases, titles)
    click.echo(table)
    click.echo(f"\nTotal datasets: {len(datasets)}")
