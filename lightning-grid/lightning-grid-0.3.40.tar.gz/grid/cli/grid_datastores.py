from typing import Optional

import click

from grid import Grid
from grid.cli.grid_train import get_credentials


@click.group(invoke_without_command=True)
@click.pass_context
def datastores(ctx) -> None:
    """Manages datastore workflows in Grid"""
    return


@datastores.command()
@click.argument('session_name', nargs=1)
@click.pass_context
def resume(ctx, session_name: str):
    """Resumes uploading a datastore"""
    client = Grid()
    if session_name == "list":
        client.list_resumable_datastore_sessions()
        return

    client.resume_datastore_session(session_name)


@datastores.command()
@click.option('--source_dir',
              type=click.Path(exists=True, file_okay=True, dir_okay=True),
              required=True,
              help='Source directory to upload datastore files')
@click.option('--name', type=str, required=True, help='Name of the datastore')
@click.option('--grid_credential',
              type=str,
              required=False,
              help='Grid credential ID that will store this datastore')
@click.option(
    '--no_compression',
    type=bool,
    required=False,
    help='If datastores should be compressed. They are compressed by default.',
    default=False,
    is_flag=True)
@click.pass_context
def create(ctx,
           source_dir: str,
           name: str,
           grid_credential: Optional[str] = None,
           no_compression: bool = False) -> None:
    """Creates datastores"""
    client = Grid()

    credential = get_credentials(client=client,
                                 grid_credential=grid_credential)

    client.upload_datastore(source_dir=source_dir,
                            credential_id=credential['credentialId'],
                            name=name,
                            no_compression=no_compression)


@datastores.command()
@click.pass_context
def list(ctx) -> None:
    """Lists datastores"""
    client = Grid()
    client.list_datastores()


@datastores.command()
@click.option('--name', type=str, required=True, help='Name of the datastore')
@click.option('--version',
              type=int,
              required=True,
              help='Version of the datastore')
@click.option('--grid_credential',
              type=str,
              required=True,
              help='Credential Id for this datastore')
@click.pass_context
def delete(ctx, name: str, version: int, grid_credential: str) -> None:
    """Lists datastores"""
    client = Grid()
    client.delete_datastore(name=name,
                            version=version,
                            credential_id=grid_credential)
