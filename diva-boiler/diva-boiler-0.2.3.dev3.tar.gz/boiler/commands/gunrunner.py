from typing import List, TextIO

import click

from boiler import cli
from boiler.commands.kw18 import _find_kw18_files, _video_name_regexp
from boiler.commands.mturk import mturk_balance
from boiler.commands.utils import activity_types_from_file
from boiler.serialization.kw18 import KW18FileSet


@click.group(name='gunrunner', short_help='Manage transitions to gunrunner')
@click.pass_obj
def gunrunner(ctx):
    pass


@gunrunner.command(name='dispatch', short_help='Dispatch a set of activities to gunrunner')
@click.argument('path', type=click.Path(exists=True, file_okay=False, resolve_path=True), nargs=-1)
@click.option('--activity-type-list', type=click.File(mode='r'), required=True)
@click.option('--recursive', '-r', is_flag=True)
@click.option('--audited/--not-audited', default=True)
@click.pass_context
def dispatch(ctx, path: List[str], recursive: bool, activity_type_list: TextIO, audited: bool):
    """Dispatch one or more videos to gunrunner.

    This command is intended to be run from the audit repository.  Because the
    list of activities from annotation -> audit is not necessarily the same,
    the user must provide the correct activity type list.  (Get the current
    list of activities with `boiler activity list-types`.)

    \b
    Example:
    boiler gunrunner dispatch -r --activity-type-list 47-activities.txt \\
        m2-annotations-audit/2018-10-15/08/
    """
    session = ctx.obj['session']
    has_error = False
    activity_types = activity_types_from_file(activity_type_list)

    if mturk_balance(session) < 500:
        click.secho(
            'The MTurk balance is below $500.  Please add more money '
            'to the account before dispatching more HITs.',
            fg='red',
        )
        ctx.exit(1)

    for base_path in _find_kw18_files(path, recursive):
        video_name_match = _video_name_regexp.search(str(base_path))
        if video_name_match is None:
            has_error = True
            click.echo(f'Could not determine video name from "{base_path}"')
            continue

        video_name = video_name_match.group()

        click.echo(f'Dispatching {video_name}...')
        kw18_file_upload = KW18FileSet.create_from_path(base_path).upload(session)

        data = {
            'video_name': video_name,
            'activity_types': activity_types,
            'kw18_file_upload_id': kw18_file_upload['id'],
            'audited': audited,
        }
        resp = session.post('video-pipeline/gunrunner/dispatch', json=data)
        try:
            response_data = resp.json()
        except Exception:
            response_data = {}

        if not resp.ok:
            message = response_data.get('error', 'Unknown error')
            click.secho(f'Failed to dispatch {video_name}', fg='red')
            click.echo(f'=> {message}')
            continue

        click.secho(f'Successfully dispatched {video_name}', fg='green')
    ctx.exit(0 if not has_error else 1)


cli.add_command(gunrunner)
