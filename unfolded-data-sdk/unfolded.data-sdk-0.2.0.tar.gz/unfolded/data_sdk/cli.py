import json
import sys
from functools import partial
from getpass import getpass
from pathlib import Path

import click
from pydantic.json import pydantic_encoder

from unfolded.data_sdk.data_sdk import DataSDK
from unfolded.data_sdk.models import MediaType


class PathType(click.Path):
    """A Click path argument that returns a pathlib Path, not a string"""
    def convert(self, value, param, ctx):
        return Path(super().convert(value, param, ctx))


@click.group()
def main():
    pass


@click.command()
def list_datasets():
    """List datasets for a given user
    """
    data_sdk = DataSDK()
    output_data = [dataset.dict() for dataset in data_sdk.list_datasets()]
    click.echo(json.dumps(output_data, indent=4, default=pydantic_encoder))


@click.command()
@click.option('--dataset-id', type=str, required=True, help='Dataset id.')
@click.option(
    '-o',
    '--output-file',
    type=PathType(file_okay=True, writable=True),
    required=True,
    help='Output file for dataset.')
def download_dataset(dataset_id, output_file):
    """Download data for existing dataset to disk
    """
    data_sdk = DataSDK()
    data_sdk.download_dataset(dataset=dataset_id, output_file=output_file)


@click.command()
@click.option(
    '-n',
    '--name',
    type=str,
    required=False,
    default=None,
    help='Dataset name.')
@click.option(
    '--media-type',
    type=click.Choice([c.value for c in MediaType], case_sensitive=False),
    required=False,
    default=None,
    help='Dataset media type.')
@click.option(
    '--desc',
    type=str,
    required=False,
    default=None,
    show_default=True,
    help='Dataset description.')
@click.argument('file', type=PathType(readable=True, file_okay=True))
def upload_file(file, name, media_type, desc):
    """Upload new dataset to Unfolded Studio
    """
    data_sdk = DataSDK()
    new_dataset = data_sdk.upload_file(
        file=file, name=name, media_type=media_type, description=desc)
    click.echo(new_dataset.json())


@click.command()
@click.option('--dataset-id', type=str, required=True, help='Dataset id.')
@click.option(
    '--media-type',
    type=click.Choice([c.value for c in MediaType], case_sensitive=False),
    required=False,
    default=None,
    help='Dataset media type.')
@click.argument('file', type=PathType(readable=True, file_okay=True))
def update_dataset(file, dataset_id, media_type):
    """Update data for existing Unfolded Studio dataset
    """
    data_sdk = DataSDK()
    updated_dataset = data_sdk.update_dataset(
        file=file, dataset=dataset_id, media_type=media_type)
    click.echo(updated_dataset.json())


def abort_if_false(ctx, param, value):
    # pylint: disable=unused-argument
    if not value:
        ctx.abort()


@click.command()
@click.option('--dataset-id', type=str, required=True, help='Dataset id.')
@click.option(
    '--force',
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    help='Delete dataset without prompting.',
    prompt='Are you sure you want to delete the dataset?')
def delete_dataset(dataset_id):
    """Delete dataset from Unfolded Studio

    Warning: This operation cannot be undone. If you delete a dataset currently
    used in one or more maps, the dataset will be removed from those maps,
    possibly causing them to render incorrectly.
    """
    data_sdk = DataSDK()
    data_sdk.delete_dataset(dataset=dataset_id)
    click.echo('Dataset deleted.', file=sys.stderr)


@click.command()
@click.option(
    '--refresh-token',
    type=str,
    help=f'Refresh Token. Retrieve from https://studio.unfolded.ai/tokens.html',
    # Use getpass for password input
    # Ref https://github.com/pallets/click/issues/300#issuecomment-606105993
    default=partial(getpass, 'Refresh Token: '))
def store_refresh_token(refresh_token):
    """Store refresh token to enable seamless future authentication

    Retrieve token from https://studio.unfolded.ai/tokens.html
    """
    DataSDK(refresh_token=refresh_token)
    click.echo('Successfully stored refresh token.')


main.add_command(list_datasets)
main.add_command(download_dataset)
main.add_command(upload_file)
main.add_command(update_dataset)
main.add_command(delete_dataset)
main.add_command(store_refresh_token)

if __name__ == '__main__':
    main()
