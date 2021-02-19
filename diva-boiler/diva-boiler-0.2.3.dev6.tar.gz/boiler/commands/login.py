import webbrowser

import click
import gitlab
from gitlab.exceptions import GitlabAuthenticationError
import requests

from boiler import BOILER_CONFIG_FILE, cli, update_config_value


def _is_valid_stumpf_token(stumpf_url: str, token: str) -> bool:
    # note - don't use the boiler session since that could have an old token,
    # and automatically fails on auth failures.
    return requests.get(stumpf_url + '/api/v1/user/me', headers={'X-Stumpf-Token': token}).ok


def _is_valid_gitlab_token(url, token):
    gl = gitlab.Gitlab(url, timeout=10, private_token=token)

    try:
        gl.auth()
    except GitlabAuthenticationError:
        return False

    return True


@click.group(name='login', short_help='authenticate with various services')
@click.pass_obj
def login(ctx):
    pass


@login.command(name='stumpf', help='authenticate with stumpf')
@click.pass_obj
def login_stumpf(ctx):
    click.echo('A browser window has been opened, login and copy the token to login.', err=True)
    webbrowser.open(ctx['stumpf_url'] + '/login?next=/token')

    while True:
        stumpf_token = click.prompt('Token', err=True)
        if _is_valid_stumpf_token(ctx['stumpf_url'], stumpf_token):
            update_config_value(BOILER_CONFIG_FILE, 'stumpf_token', stumpf_token)
            return click.echo(click.style('You are now logged in.', fg='green'), err=True)
        else:
            click.echo(
                click.style(
                    "Your token doesn't appear to be valid, did you copy/paste correctly?",
                    fg='yellow',
                ),
                err=True,
            )


@login.command(name='kwgitlab', help='authenticate with kwgitlab')
@click.pass_obj
def login_kwgitlab(ctx):
    click.echo(
        'A browser window has been opened, login and create a token with the api and \n'
        'read_user scopes and paste it here:',
        err=True,
    )
    webbrowser.open(f"{ctx['gitlab_url']}/profile/personal_access_tokens")

    while True:
        kwgitlab_token = click.prompt('personal access token', err=True)

        if _is_valid_gitlab_token(ctx['gitlab_url'], kwgitlab_token):
            update_config_value(BOILER_CONFIG_FILE, 'kwgitlab_token', kwgitlab_token)
            return click.echo(click.style('You are now authenticated.', fg='green'), err=True)
        else:
            click.echo(
                click.style(
                    "Your token doesn't appear to be valid, did you copy/paste correctly?",
                    fg='yellow',
                ),
                err=True,
            )


cli.add_command(login)
