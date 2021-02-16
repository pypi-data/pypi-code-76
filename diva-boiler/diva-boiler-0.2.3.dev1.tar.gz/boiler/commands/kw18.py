from pathlib import Path
import re
from typing import Any, Dict, Iterator, List, Set, TextIO, Tuple

import click
from git import InvalidGitRepositoryError, Repo

from boiler import cli
from boiler.commands.utils import activity_types_from_file, summarize_activities
from boiler.serialization.kw18 import KW18FileSet
from boiler.validate import validate_activities

_video_name_regexp = re.compile(
    r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'
    r'\.(?P<start_hour>\d{2})-(?P<start_minute>\d{2})-(?P<start_second>\d{2})'
    r'\.(?P<end_hour>\d{2})-(?P<end_minute>\d{2})-(?P<end_second>\d{2})'
    r'\.(?P<location>[^./]+)'
    r'\.(?P<gtag>G[^./\\]+)'
)
GENERIC_ERROR = 'Something went wrong communicating with the server...'


def _find_kw18_files(paths: List[str], recursive: bool) -> Iterator[Path]:
    if recursive:
        for p in paths:
            for g in Path(p).glob('**/*.kw18'):
                yield g.parent
    else:
        for p in paths:
            yield Path(p)


def _validate_kw18(path: Path) -> Tuple[List[str], List[str], Dict[str, Any]]:
    kw18_file_set = KW18FileSet.create_from_path(path)
    try:
        activity_list = kw18_file_set.read()
    except Exception as err:
        return [], [str(err)], {}

    summary = summarize_activities(activity_list)
    warnings, errors = validate_activities(activity_list)
    return [str(x) for x in warnings], [str(x) for x in errors], summary


def get_suffix(count: int, singular: str, plural: str) -> str:
    if count == 1:
        return singular
    return plural


def _get_repo_path(path: Path) -> str:
    """Return the path relative to the git repo root directory."""
    path = path.absolute()
    try:
        repo = Repo(path, search_parent_directories=True)
    except InvalidGitRepositoryError:
        click.echo('Could not find the git repository.  Is this file inside the annotation repo?')
        raise

    return path.relative_to(repo.working_tree_dir).as_posix()


def _serialize_summary(summary: Dict[str, Any], indent: str) -> List[str]:
    default_dict = {'count': 0, 'by_type': []}
    activities = summary.get('activities', default_dict)
    actors = summary.get('actors', default_dict)

    content: List[str] = []

    count = activities['count']
    a = get_suffix(count, 'activity', 'activities')
    content.append(f'{indent}{count} {a}')
    for activity in activities['by_type']:
        name = activity['name']
        count = activity['count']
        content.append(f'{indent}  * {name} ({count})')

    count = actors['count']
    a = get_suffix(count, 'actor', 'actors')
    content.append(f'{indent}{count} {a}')
    for actor in actors['by_type']:
        name = actor['name']
        count = actor['count']
        content.append(f'{indent}  * {name} ({count})')

    return content


def _serialize_output(
    path: Path, error: List[str], warning: List[str], summary: Dict[str, Any],
) -> str:
    prefix = click.style(str(path), bold=True)
    content: List[str] = []
    if error:
        mark = click.style(f'✗  {prefix}', fg='red')
    elif warning:
        mark = click.style(f'⚠  {prefix}', fg='yellow')
    else:
        mark = click.style(f'✔️  {prefix}', fg='green')

    content.extend(
        [
            # str(path),  TODO: maybe add a verbose option for full path
            mark
        ]
    )
    indent = ' ' * 4

    for e in error:
        content.append(click.style(f'{indent}{e}', fg='red'))

    for w in warning:
        content.append(click.style(f'{indent}{w}', fg='yellow'))

    content.extend(_serialize_summary(summary, indent))

    return '\n'.join(content)


@click.group(name='kw18', short_help='Ingest and validate kw18')
@click.pass_obj
def kw18(ctx):
    pass


@kw18.command(name='validate', help='validate one or more kw18 annotations')
@click.argument(
    'path',
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    nargs=-1,
    required=True,
)
@click.option('--recursive', '-r', is_flag=True)
@click.option('--error-only', is_flag=True, help='Only output information on validation failure')
@click.pass_context
def validate(ctx, path: List[str], recursive: bool, error_only: bool):
    has_invalid = False
    for base_path in _find_kw18_files(path, recursive):
        try:
            warning, error, summary = _validate_kw18(base_path)
        except FileNotFoundError:
            warning = []
            summary = {}
            error = ['Could not determine kw18 file']

        try:
            p = next(base_path.glob('*.kw18'))
        except StopIteration:
            p = base_path.absolute()

        if error_only:
            warning = []

        if error or not error_only:
            click.echo(_serialize_output(path=p, error=error, warning=warning, summary=summary))
            click.echo('')

    ctx.exit(0 if not has_invalid else 1)


@kw18.command(name='dispatch', short_help='dispatch annotation tasks from existing kw18 files')
@click.argument(
    'path',
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    nargs=-1,
    required=True,
)
@click.option('--recursive', '-r', is_flag=True)
@click.option('--vendor', type=click.STRING, required=True, help='the annotation vendor')
@click.option(
    '--activity-type-list',
    type=click.File(mode='r'),
    required=True,
    help='the activity types annotated',
)
@click.option('--set-name', type=click.STRING, required=True)
@click.pass_context
def dispatch(
    ctx, path: List[str], recursive: bool, vendor: str, activity_type_list: TextIO, set_name: str
):
    session = ctx.obj['session']
    has_error = False
    activity_types = activity_types_from_file(activity_type_list)
    for base_path in _find_kw18_files(path, recursive):
        video_name_match = _video_name_regexp.search(str(base_path))
        if video_name_match is None:
            has_error = True
            click.echo(f'Could not determine video name from "{base_path}"')
            continue

        repo_path = _get_repo_path(base_path)
        data = {
            'vendor_name': vendor,
            'activity_types': activity_types,
            'set_name': set_name,
            'annotation_repo_path': repo_path,
            'video_name': video_name_match.group(),
        }
        r = session.post('video-pipeline/annotate', json=data)
        try:
            response_data = r.json()
        except Exception:
            response_data = {}

        if r.status_code == 201:
            click.secho(f'Dispatched {repo_path}', fg='green')
        else:
            message = response_data.get('error', GENERIC_ERROR)
            has_error = True
            click.secho(f'Error dispatching {repo_path}', fg='red')
            click.echo(f'=> {message}')
        click.echo('')

    ctx.exit(0 if not has_error else 1)


@kw18.command(name='ingest', short_help='push files from the annotation repository')
@click.argument(
    'path',
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    nargs=-1,
    required=True,
)
@click.option('--recursive', '-r', is_flag=True)
@click.pass_context
def ingest(ctx, path, recursive):
    """Ingest one or more annotations from the annotation repository.

    This command takes a set of KW18 annotation files from the provided paths
    and sends them to Stumpf.  Stumpf will first detect whether the files have
    changed or not.  If they have not, no further action will be taken.  If
    they have, then Stumpf will:

    \b
    1. Generate a transition to the "annotation" status
    2. Run server side validation.
    3. If validation fails, return failure information.
    4. If validation succeeds, transition to the "audit" state
       and ingest activities from the KW18 files.
    """
    session = ctx.obj['session']
    for base_path in _find_kw18_files(path, recursive):
        repo_path = _get_repo_path(base_path)
        try:
            warning, error, summary = _validate_kw18(base_path)
        except FileNotFoundError:
            warning = []
            summary = {}
            error = ['Could not determine kw18 file']

        click.echo(
            _serialize_output(path=Path(repo_path), error=error, warning=warning, summary=summary)
        )
        click.echo('')

        kw18_file_upload = KW18FileSet.create_from_path(base_path).upload(session)
        repo_path = _get_repo_path(base_path)

        data = {
            'annotation_repo_path': repo_path,
            'kw18_file_upload_id': kw18_file_upload['id'],
        }

        r = session.post('video-pipeline/process-annotation', json=data)
        try:
            response_data = r.json()
        except Exception:
            response_data = {}

        if not r.ok:
            message = response_data.get('error', GENERIC_ERROR)
            click.secho('Error uploading annotations', fg='red')
            click.echo(f'=> {message}')
            click.echo('')
            continue

        status_changes = response_data.get('status_changes')
        if status_changes:
            recorded: Set[str] = set()
            click.echo('Status changes:')
            for sc in status_changes:
                sc_formatted = f'{sc["old_status"]} => {sc["new_status"]}'
                if sc_formatted not in recorded:
                    click.echo(f'    * {sc_formatted}')
                    recorded.add(sc_formatted)
        else:
            click.echo('  No file changes detected')

        click.echo('')


cli.add_command(kw18)
