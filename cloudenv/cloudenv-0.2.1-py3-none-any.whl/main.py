# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import io
import logging
import os
import sys
import subprocess

from os.path import expanduser
from contextlib import contextmanager
from io import StringIO
from dotenv import dotenv_values

from .compat import PY2, StringIO, to_env
from .version import __version__

logger = logging.getLogger(__name__)

def with_warn_for_invalid_lines(mappings):
    # type: (Iterator[Binding]) -> Iterator[Binding]
    for mapping in mappings:
        if mapping.error:
            logger.warning(
                "cloudenv could not parse statement starting at line %s",
                mapping.original.line,
            )
        yield mapping


class Cloudenv():

    def __init__(self, bearer_file, secret_key_file, override=True):
        self.bearer_file = bearer_file
        self.secret_key_file = secret_key_file
        self._dict = None
        self.api_host = "https://app.cloudenv.com"
        self.read_path = "/api/v1/envs"
        self.override = override

    def dict(self):
        if self._dict:
            return self._dict

        if 'PYTHON_ENV' in os.environ.keys():
            self._dict = self.parse(os.environ['PYTHON_ENV'])
            self._dict.update(self.parse('default'))
        else:
            self._dict = self.parse('default')

        return self._dict

    def parse(self, environment):
        stdout = subprocess.getoutput('curl -s -H "Authorization: Bearer {0}" "{1}{2}?name={3}&environment={4}&version={5}&lang=python" | openssl enc -a -aes-256-cbc -md sha512 -d -pass pass:"{6}" 2> /dev/null'.format(self.bearer(), self.api_host, self.read_path, self.app_name(), environment, __version__, self.secret_key()))
        filelike = StringIO(stdout)
        filelike.seek(0)
        return dotenv_values(stream=filelike)

    def bearer(self):
        return os.getenv('CLOUDENV_BEARER_TOKEN') or open(self.bearer_file, 'r').read().strip()

    def secret_key(self):
        return open(self.secret_key_file, 'r').read().split('\n')[1].split()[1]

    def app_name(self):
        return open(self.secret_key_file, 'r').read().split('\n')[0].split()[1]

    def set_as_environment_variables(self):
        """
        Load the current cloudenv as system environemt variable.
        """
        for k, v in self.dict().items():
            if k in os.environ and not self.override:
                continue
            if v is not None:
                os.environ[to_env(k)] = to_env(v)

        return True

    def get(self, key):
        data = self.dict()

        if key in data:
            return data[key]

        if self.verbose:
            logger.warning("Key %s not found in %s.", key, self.cloudenv_path)

        return None

def _walk_to_root(path):
    """
    Yield directories starting from the given directory up to the root
    """
    if not os.path.exists(path):
        raise IOError('Starting path not found')

    if os.path.isfile(path):
        path = os.path.dirname(path)

    last_dir = None
    current_dir = os.path.abspath(path)
    while last_dir != current_dir:
        yield current_dir
        parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
        last_dir, current_dir = current_dir, parent_dir


def find_cloudenv_bearer(filename='.cloudenvrc', raise_error_if_not_found=True):
    """
    Search in increasingly higher folders for the given file

    Returns path to the file if found, or an empty string otherwise
    """

    # will work for .py files
    frame = sys._getframe()
    # find first frame that is outside of this file
    if PY2 and not __file__.endswith('.py'):
        # in Python2 __file__ extension could be .pyc or .pyo (this doesn't account
        # for edge case of Python compiled for non-standard extension)
        current_file = __file__.rsplit('.', 1)[0] + '.py'
    else:
        current_file = __file__

    while frame.f_code.co_filename == current_file:
        assert frame.f_back is not None
        frame = frame.f_back
    frame_filename = frame.f_code.co_filename
    path = os.path.dirname(os.path.abspath(frame_filename))

    for dirname in _walk_to_root(path):
        check_path = os.path.join(dirname, filename)
        if os.path.isfile(check_path):
            return check_path

    for dirname in _walk_to_root(expanduser("~")):
        check_path = os.path.join(dirname, filename)
        if os.path.isfile(check_path):
            return check_path

    if raise_error_if_not_found:
        raise IOError('Cloudenv bearer token file not found (should be at .cloudenvrc)')

    return ''

def find_cloudenv_secret_key(filename='.cloudenv-secret-key', raise_error_if_not_found=True):
    """
    Search in increasingly higher folders for the given file

    Returns path to the file if found, or an empty string otherwise
    """

    # will work for .py files
    frame = sys._getframe()
    # find first frame that is outside of this file
    if PY2 and not __file__.endswith('.py'):
        # in Python2 __file__ extension could be .pyc or .pyo (this doesn't account
        # for edge case of Python compiled for non-standard extension)
        current_file = __file__.rsplit('.', 1)[0] + '.py'
    else:
        current_file = __file__

    while frame.f_code.co_filename == current_file:
        assert frame.f_back is not None
        frame = frame.f_back
    frame_filename = frame.f_code.co_filename
    path = os.path.dirname(os.path.abspath(frame_filename))

    for dirname in _walk_to_root(path):
        check_path = os.path.join(dirname, filename)
        if os.path.isfile(check_path):
            return check_path

    if raise_error_if_not_found:
        raise IOError('Cloudenv secret key file not found (should be at .cloudenv-secret-key)')

    return ''


def load_cloudenv(cloudenv_bearer=None, cloudenv_secret_key=None, override=False):
    """Get your cloudenv variables and then load all the variables found as environment variables.

    - *cloudenv_bearer*: absolute or relative path to .env file.
    - *cloudenv_secret_key*: absolute or relative path to .env file.
    - *override*: where to override the system environment variables with the variables in `.env` file.
                  Defaults to `False`.
    """
    bearer_file = cloudenv_bearer or os.getenv('CLOUDENV_BEARER_TOKEN') or find_cloudenv_bearer()
    secret_key_file = cloudenv_secret_key or find_cloudenv_secret_key()
    cloudenv = Cloudenv(bearer_file, secret_key_file, override=override)
    return cloudenv.set_as_environment_variables()


def cloudenv_values(cloudenv_bearer=None, cloudenv_secret_key=None):
    bearer_file = cloudenv_bearer or os.getenv('CLOUDENV_BEARER_TOKEN') or find_cloudenv_bearer()
    secret_key = cloudenv_secret_key or find_cloudenv_secret_key()
    cloudenv = Cloudenv(bearer_file, secret_key_file, override=True)
    return cloudenv.dict()
