"""Unearthed CLI Authentiation Commands."""
import os
import json
import logging
import sys

import click
from botocore.exceptions import ClientError

import warnings
with warnings.catch_warnings():
    # this will suppress all warnings in this block
    warnings.filterwarnings('ignore', message='int_from_bytes is deprecated')
    from unearthed.cli.auth import authorize, cognito_session

logger = logging.getLogger(__name__)


def _validate_username(ctx, param, value):
    """Prompt for username if not found in environment."""
    if value is None:
        return click.prompt('Unearthed Login Email',
                            default=cognito_session.username)
    else:
        print('Found UNEARTHED_USERNAME environment variable')
        return value


def _validate_password(ctx, param, value):
    """Prompt for password if not found in environment."""
    if value is None:
        return click.prompt('Unearthed Login Password',
                            hide_input=True)
    else:
        print('Found UNEARTHED_PASSWORD environment variable')
        return value


@click.command()
@click.option('--username', callback=_validate_username,
              envvar='UNEARTHED_USERNAME')
@click.option('--password', callback=_validate_password,
              envvar='UNEARTHED_PASSWORD')
def login(username, password):
    """Login to Unearthed."""
    logger.debug('login')

    # force a token refresh if possible
    cognito_session.check_token()
    if username == cognito_session.username:
        return print(f'Already logged in to Unearthed as {username}')

    try:
        cognito_session.username = username
        cognito_session.authenticate(password)
        print(f'Successfully logged in to Unearthed as {username}!')
    except ClientError as e:
        print(e.response['message'])


@click.command()
def logout():
    """Logout of Unearthed."""
    logger.debug('logout')
    cognito_session.logout()
    print('You are now logged out of Unearthed.')


@click.group()
def auth():
    """Manage authentication."""
    pass


@auth.command('whoami')
def whoami():
    """Display current username."""
    logger.debug('whoami')
    cognito_session.check_token()
    print(cognito_session.username)


@auth.group()
def tokens():
    """Display authentication tokens."""
    pass


@tokens.command()
def access():
    """Display the decoded Access Token."""
    logger.debug('access')
    print(json.dumps(cognito_session.decoded_access_token(), indent=2))


@tokens.command()
def id():
    """Display the decoded Id Token."""
    logger.debug('id')
    print(json.dumps(cognito_session.decoded_id_token(), indent=2))
