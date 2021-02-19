# pylint: disable=too-many-locals

"""CLI 'publish' command"""

# standard
from datetime import datetime
from pathlib import Path
import re
import uuid
# external
import click
from nbconvert import MarkdownExporter
from traitlets.config import Config
import yaml
# local
from matatika.cli.utility import create_table, Resolver
from matatika.dataset import Dataset
from .root import matatika

NOTEBOOK = ['.ipynb']
YAML = ['.yml', '.yaml']
SUPPORTED_FILETYPES = NOTEBOOK + YAML


@matatika.command('publish', short_help='Publish one or more dataset(s)')
@click.pass_context
@click.argument('dataset-file', type=click.Path(exists=True))
@click.option("--workspace-id", "-w", type=click.UUID, help="Workspace ID")
def publish(ctx, dataset_file, workspace_id):
    """Publish one or more dataset(s) from a YAML file into a workspace"""

    ctx.obj['workspace_id'] = workspace_id
    client = Resolver(ctx).client()

    file_ext = Path(dataset_file).suffix
    datasets = []

    if file_ext not in SUPPORTED_FILETYPES:
        click.secho("Filetype not supported", fg='red')
        return

    if file_ext in YAML:
        with open(dataset_file, 'r') as yaml_file:
            yaml_datasets = yaml.safe_load(yaml_file)['datasets']

        for alias in yaml_datasets:
            yaml_datasets[alias].update({'alias': alias})
            dataset = Dataset.from_dict(yaml_datasets[alias])
            datasets.append(dataset)

    elif file_ext in NOTEBOOK:
        config = Config()
        config.TemplateExporter.exclude_output_prompt = True
        config.TemplateExporter.exclude_input = True
        config.TemplateExporter.exclude_input_prompt = True
        config.ExtractOutputPreprocessor.enabled = False
        md_exporter = MarkdownExporter(config=config)
        md_str, _resources = md_exporter.from_file(dataset_file)

        match = re.search(r'#+\s(.+)', md_str)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        default_title = f"Generated Report ({timestamp})"
        dataset_title = match.group(1) if match else default_title

        dataset = Dataset.from_dict({
            'id': str(uuid.uuid4()),
            'title': dataset_title,
            'description': md_str
        })
        datasets.append(dataset)

    published_datasets = client.publish(datasets)

    click.secho(f"Successfully published {len(published_datasets)} dataset(s)\n",
                fg='green')

    ids = ['DATASET ID']
    aliases = ['ALIAS']
    titles = ['TITLE']
    statuses = ['STATUS']

    for dataset, status_code in published_datasets:
        if status_code == 201:
            status = click.style("NEW", fg='magenta')
        else:
            status = click.style("UPDATED", fg='cyan')

        if not dataset.alias:
            dataset.alias = click.style(str(dataset.alias), fg='yellow')

        ids.append(dataset.dataset_id)
        aliases.append(dataset.alias)
        titles.append(dataset.title)
        statuses.append(status)

    table = create_table(ids, aliases, titles, statuses)
    click.echo(table)
