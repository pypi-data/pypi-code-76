import os
import json
import yaml
import click

from mcutk.projects_scanner import find_projects


@click.command('scan', short_help='projects scanner')
@click.argument('path', required=True, type=click.Path(exists=True))
@click.option('-o', '--output', type=click.Path(exists=False), help='dump scan results to file, file format support: json or yml.')
@click.option('--dapeng', is_flag=True, default=False, hidden=True, help='dump for dapeng style, casfile.yml')
def cli(path, output, dapeng):
    """Scan projects from specificed directory and dump to file(json or yml)."""

    projects, count = find_projects(path, True)
    dataset = list()

    if output:
        extension = os.path.basename(output).split(".")[-1]
        for tname, plist in projects.items():
            for project in plist:
                dataset.append(project.to_dict())

        if extension in ('yml', 'yaml'):
            with open(output, 'w') as file:
                yaml.safe_dump(dataset, file, default_flow_style=False)
        else:
            with open(output, 'w') as file:
                json.dump(dataset, file)

        # elif format == 'dapeng':
        #     for project in projects:
        #         if project.path
        # else:
        #     pass

        click.echo("output file: %s" % output)
