import datetime
import json
import os
import platform
import sys
import traceback
from typing import Any, Optional
from urllib.parse import urlparse


import click
from packaging.version import parse as parse_version
from pkg_resources import DistributionNotFound, get_distribution
import requests
from requests.exceptions import RequestException
from requests_toolbelt.sessions import BaseUrlSession
import sentry_sdk
from sentry_sdk import capture_exception, configure_scope, push_scope  # type: ignore
from xdg import BaseDirectory

__version__ = None
try:
    __version__ = get_distribution('diva-boiler').version
except DistributionNotFound:
    pass

BOILER_CONFIG_PATH = __name__
BOILER_CONFIG_FILE = 'config'
SENTRY_DSN = 'https://639591f20e1148c3a65e5e9237c6afc1@o157137.ingest.sentry.io/5224648'


class BoilerException(Exception):
    pass


class BoilerWarning(BoilerException):
    pass


class BoilerError(BoilerException):
    pass


class BoilerSession(BaseUrlSession):

    page_size = 50

    def __init__(self, base_url: str, token: Optional[str]):
        base_url = f'{base_url.rstrip("/")}/'  # tolerate input with or without trailing slash
        super(BoilerSession, self).__init__(base_url=base_url)
        if token:
            token = token.strip()
        self.token = token
        self.headers.update(
            {
                'User-agent': f'boiler/{__version__}',
                'Accept': 'application/json',
                'X-Stumpf-Token': self.token,
            }
        )

    def request(self, *args, **kwargs):
        response = super().request(*args, **kwargs)

        if response.status_code in [401, 403]:
            click.echo(
                click.style(
                    "You are attempting to perform an authorized operation but you aren't logged in.\n"  # noqa
                    'Run the following command: boiler login stumpf',
                    fg='yellow',
                ),
                err=True,
            )
            sys.exit(1)

        return response


def newer_version_available():
    if __version__ is None:
        return False

    this_version = parse_version(__version__)
    if this_version.is_devrelease:
        return False

    r = requests.get('https://pypi.org/pypi/diva-boiler/json', timeout=(5, 5))
    r.raise_for_status()
    releases = [parse_version(v) for v in r.json()['releases'].keys()]
    for release in releases:
        if not (release.is_prerelease or release.is_devrelease) and release > this_version:
            return True
    return False


def main():
    try:
        # make boiler configuration directory
        BaseDirectory.save_config_path(BOILER_CONFIG_PATH)
        cli()
    except Exception as e:
        click.echo(
            click.style(
                'The following unexpected error occurred while attempting your operation:\n',
                fg='red',
            ),
            err=True,
        )

        click.echo(traceback.format_exc(), err=True)

        click.echo(f'boiler:  v{__version__}', err=True)
        click.echo(f'python:  v{platform.python_version()}', err=True)
        click.echo(f'time:    {datetime.datetime.now(datetime.timezone.utc).isoformat()}', err=True)
        click.echo(f'os:      {platform.platform()}', err=True)
        click.echo(f'command: {" ".join(sys.argv[1:])}\n', err=True)

        click.echo(
            click.style(
                'This is a bug in boiler and has already been reported. '
                'If you would like to add any detail you can open an issue below.',
                fg='yellow',
            ),
            err=True,
        )
        click.echo(
            'https://gitlab.com/diva-mturk/stumpf-diva/issues/new', err=True,
        )

        with push_scope() as scope:
            scope.set_extra('boiler_version', f'v{__version__}')
            scope.set_extra('python_version', f'v{platform.python_version()}')
            scope.set_extra('os', f'{platform.platform()}')
            scope.set_extra('command', f'{" ".join(sys.argv[1:])}')
            capture_exception(e)


def update_config_value(filename: str, key: str, value: Any) -> None:
    config_dir = BaseDirectory.load_first_config(BOILER_CONFIG_PATH)
    config_file = os.path.join(config_dir, filename)

    if os.path.exists(config_file):
        with open(config_file, 'r') as infile:
            config = json.load(infile)
            config[key] = value
    else:
        config = {key: value}

    with open(config_file, 'w') as outfile:
        json.dump(config, outfile, indent=4)


def get_config_value(filename: str, key: str) -> Optional[Any]:
    config_dir: Optional[str] = BaseDirectory.load_first_config(BOILER_CONFIG_PATH)

    if config_dir:
        config_file = os.path.join(config_dir, BOILER_CONFIG_FILE)

        if os.path.exists(config_file):
            with open(config_file, 'r') as infile:
                config = json.load(infile)
                return config.get(key)

    return None


@click.group()
@click.option(
    '--api-url', default='https://stumpf.avidannotations.com/api/diva/', envvar='STUMPF_API_URL',
)
@click.option(
    '--x-stumpf-token',
    envvar='X_STUMPF_TOKEN',
    default=get_config_value(BOILER_CONFIG_FILE, 'stumpf_token'),
)
@click.option('--offline', is_flag=True)
@click.option(
    '--gitlab-url', envvar='GITLAB_URL', default='https://kwgitlab.kitware.com', hidden=True
)
@click.option(
    '--gitlab-project-id', type=click.INT, envvar='GITLAB_PROJECT_ID', default=497, hidden=True
)
@click.version_option()
@click.pass_context
def cli(ctx, api_url, x_stumpf_token, offline, gitlab_url, gitlab_project_id):
    api = urlparse(api_url)

    if api.netloc == 'stumpf.avidannotations.com':
        sentry_sdk.init(SENTRY_DSN)  # type: ignore

    if not offline:
        try:
            if newer_version_available():
                click.echo(
                    click.style(
                        """There is a newer version of boiler available.
You must upgrade to the latest version before continuing.
If you are using pipx, then you can upgrade by running the following command:
""",
                        fg='yellow',
                    ),
                    err=True,
                )
                click.echo(click.style('pipx upgrade diva-boiler', fg='green'), err=True)
                sys.exit(1)
        except RequestException:
            click.echo(
                click.style('Failed to check for newer version of boiler:', fg='red'), err=True
            )
            raise

    # remove old text config file at 'credentials'
    # this isn't strictly necessary, it just cleans up an unused file on their machine.
    # TODO: remove this after a short period
    config_dir = BaseDirectory.load_first_config(BOILER_CONFIG_PATH)
    if os.path.exists(os.path.join(config_dir, 'credentials')):
        os.remove(os.path.join(config_dir, 'credentials'))

    session = BoilerSession(api_url, x_stumpf_token)
    ctx.obj = {
        'session': session,
        'stumpf_url': api_url.replace('/api/diva', '').rstrip('/'),
        'gitlab_url': gitlab_url.rstrip('/'),
        'gitlab_project_id': gitlab_project_id,
    }

    # set current user under sentry
    # ignore any error from requests since the user may be trying to perform a local operation
    with configure_scope() as scope:
        try:
            user = requests.get(
                f'{ctx.obj["stumpf_url"]}/api/v1/user/me',
                headers={'X-Stumpf-Token': x_stumpf_token},
                timeout=(5, 5),
            )

            if user.ok:
                scope.user = user.json()
        except RequestException:
            pass


# TODO: re-enable kpf once deserialization is fixed
from boiler.commands import (  # noqa: F401 E402
    activity,
    export,
    gunrunner,
    janitor,
    kw18,
    login,
    mturk,
    vendor,
    video,
)
