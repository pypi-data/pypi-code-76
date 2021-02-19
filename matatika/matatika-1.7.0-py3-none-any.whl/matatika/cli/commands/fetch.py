"""CLI 'fetch' command"""

import click
from matatika.cli.utility import Resolver
from matatika.types import DATA_FORMAT
from matatika.uuid import is_uuid4
from .root import matatika


@matatika.command("fetch", short_help="Fetch the data from a dataset")
@click.pass_context
@click.argument("dataset-id-or-alias")
@click.option("--as", 'as_', type=DATA_FORMAT, required=False, default='RAW')
@click.option("--workspace-id", "-w", type=click.UUID, help="Workspace ID")
@click.option("--output-file", "-f", type=click.Path(writable=True), help="Output file path")
def fetch(ctx, dataset_id_or_alias, as_, workspace_id, output_file):
    """Fetch the data from a dataset"""

    ctx.obj['workspace_id'] = workspace_id

    exclude_vars = {}

    # when an ID is provided, we don't need a workspace ID
    if is_uuid4(dataset_id_or_alias):
        exclude_vars['workspace_id'] = None

    client = Resolver(ctx).client(**exclude_vars)

    data = client.fetch(dataset_id_or_alias, data_format=as_)

    if output_file:
        with open(output_file, "w") as file_:
            file_.write(data)
        click.secho(f"Dataset {dataset_id_or_alias} data successfully written to {output_file}",
                    fg='green')

    else:
        click.secho(f"*** START DATASET {dataset_id_or_alias} DATA CHUNK STDOUT DUMP ***",
                    err=True,  fg='yellow')
        click.echo(data)
        click.secho(f"*** END DATASET {dataset_id_or_alias} DATA CHUNK STDOUT DUMP ***",
                    err=True,  fg='yellow')
