from pathlib import Path

import click

from unfolded.data_sdk.data_sdk import DataSDK


class PathType(click.Path):
    """A Click path argument that returns a pathlib Path, not a string"""
    def convert(self, value, param, ctx):
        return Path(super().convert(value, param, ctx))


@click.group()
def main():
    pass


token_opt = click.option(
    '--token', type=str, required=True, help='Unfolded Studio access token.')
baseurl_opt = click.option(
    '--baseurl',
    type=str,
    required=False,
    default='https://api.unfolded.ai',
    show_default=True,
    help='Unfolded Studio API URL.')


@click.command()
@token_opt
@baseurl_opt
def list_datasets(token, baseurl):
    """List datasets for a given user
    """
    data_sdk = DataSDK(token=token, baseurl=baseurl)
    for dataset in data_sdk.list_datasets():
        click.echo(dataset.json(indent=4))


@click.command()
@click.option('--dataset-id', type=str, required=True, help='Dataset id.')
@click.option(
    '-o',
    '--output-file',
    type=PathType(file_okay=True, writable=True),
    required=True,
    help='Output file for dataset.')
@token_opt
@baseurl_opt
def download_dataset(dataset_id, output_file, token, baseurl):
    """Download data for existing dataset to disk
    """
    data_sdk = DataSDK(token=token, baseurl=baseurl)
    data_sdk.download_dataset(dataset=dataset_id, output_file=output_file)


@click.command()
@click.option('-n', '--name', type=str, required=True, help='Dataset name.')
@click.option(
    '--content-type',
    type=str,
    required=False,
    default=None,
    help='Dataset content type.')
@click.option(
    '--desc',
    type=str,
    required=False,
    default=None,
    show_default=True,
    help='Dataset description.')
@click.argument('file', type=PathType(readable=True, file_okay=True))
@token_opt
@baseurl_opt
def upload_file(file, name, content_type, desc, token, baseurl):
    """Upload new dataset to Unfolded Studio
    """
    data_sdk = DataSDK(token=token, baseurl=baseurl)
    data_sdk.upload_file(
        file=file, name=name, content_type=content_type, description=desc)


@click.command()
@click.option('--dataset-id', type=str, required=True, help='Dataset id.')
@click.option(
    '--content-type',
    type=str,
    required=False,
    default=None,
    help='Dataset content type.')
@click.argument('file', type=PathType(readable=True, file_okay=True))
@token_opt
@baseurl_opt
def update_dataset(file, dataset_id, content_type, token, baseurl):
    """Update data for existing Unfolded Studio dataset
    """
    data_sdk = DataSDK(token=token, baseurl=baseurl)
    data_sdk.update_dataset(
        file=file, dataset=dataset_id, content_type=content_type)


@click.command()
@click.option('--dataset-id', type=str, required=True, help='Dataset id.')
@token_opt
@baseurl_opt
def delete_dataset(dataset_id, token, baseurl):
    """Delete dataset from Unfolded Studio

    Warning: This operation cannot be undone. If you delete a dataset currently
    used in one or more maps, the dataset will be removed from those maps,
    possibly causing them to render incorrectly.
    """
    data_sdk = DataSDK(token=token, baseurl=baseurl)
    data_sdk.delete_dataset(dataset=dataset_id)


main.add_command(list_datasets)
main.add_command(download_dataset)
main.add_command(upload_file)
main.add_command(update_dataset)
main.add_command(delete_dataset)

if __name__ == '__main__':
    main()
