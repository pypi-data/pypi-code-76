from pathlib import Path
from typing import List

import click

from boiler import cli


@click.group('export', short_help='save current annotation data as kpf files')
def export():
    pass


@export.command(name='video', short_help='export data by video name')
@click.argument('video', nargs=-1)
@click.option(
    '--output', type=click.Path(exists=True, file_okay=False, resolve_path=True), default='.'
)
@click.option('--force/--no-force', help='overwrite existing files', default=False)
@click.pass_context
def video(ctx, output: str, video: List[str], force: bool):
    session = ctx.obj['session']
    success = True
    for video_name in video:
        resp = session.get('video', params={'name': video_name})
        output_path = Path(output) / f'{video_name}.zip'

        if output_path.exists() and not force:
            click.echo(f'A file already exists at {output_path}')
            success = False
            continue

        if resp.status_code != 200 or not resp.json():
            click.echo(f'Could not find {video_name}')
            success = False
            continue

        video_id = resp.json()[0]['id']

        click.echo(f'Downloading {output_path}...')
        resp = session.get(f'video/{video_id}/kpf')
        if resp.status_code != 200:
            click.echo(f'Error downloading {video_name}')
            success = False
            continue

        with output_path.open('wb') as f:
            f.write(resp.content)

    ctx.exit(0 if success else 1)


cli.add_command(export)
