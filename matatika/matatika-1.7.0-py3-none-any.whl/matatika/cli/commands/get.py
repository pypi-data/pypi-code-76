"""CLI 'get' command and subcommands"""

import click
from matatika.cli.utility import Resolver
from .root import matatika


@matatika.group('get', short_help='Get a specific resource')
def get():
    """Display a specific resource"""


@get.command('dataset', short_help='Get a dataset')
@click.pass_context
@click.argument('dataset-id', type=click.UUID)
def get_dataset(ctx, dataset_id):
    """Display a dataset resource"""

    client = Resolver(ctx).client()
    dataset = client.get_dataset(dataset_id, raw=True)

    click.echo(dataset)
