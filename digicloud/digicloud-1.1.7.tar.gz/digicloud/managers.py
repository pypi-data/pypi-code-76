"""
    Managers definition.
"""
import os
import pickle
import sys
from pathlib import Path
from collections import ChainMap
from json import JSONDecodeError

import yaml
from requests import Session as Sess, HTTPError


class ConfigManager():
    """Configuration manager for all configs."""
    FILE_NAME = 'config'
    DEFAULTS = {
        'BASE_URL': os.environ.get('API_BASE_URL', "https://api.digicloud.ir"),
    }

    def __init__(self, app_logger):
        self._log = app_logger
        self._path = self._get_config_path()
        self._states = dict()
        self._load()

    def __getitem__(self, item):
        try:
            return ChainMap(self.DEFAULTS, self._states).get(item)
        except KeyError:
            raise f'No "{item}" in configuration.'

    def __setitem__(self, item, value):
        self._states[item] = value

    def __delitem__(self, item):
        if item in self._states:
            del self._states[item]

    def __contains__(self, item):
        return item in self._states

    def __call__(self):
        return self._states

    def _get_config_path(self):
        """Create config file directory.

        Handles platform dependent path creation for ``FILE_NAME ``,
        and return full path to config file.
        """
        path = {
            'darwin': '$HOME/Library/Application Support/digicloud',
            'win': '%LOCALAPPDATA%/digicloud',
            'linux': '$HOME/.config/digicloud',
        }[sys.platform]

        path = os.path.expandvars(path)

        if not os.path.isdir(path):
            self._log.debug('No config director found.')
            try:
                os.mkdir(path, mode=0o755)
                self._log.debug(f'Config dir made in "{path}".')
            except IOError:
                raise "Create config path failes."

        full_path = os.path.join(path, self.FILE_NAME)
        Path(full_path).touch()

        return full_path

    def _load(self):
        with open(self._path, 'rb') as file_:
            if os.path.getsize(self._path) > 0:
                self._states = pickle.load(file_)

    def _dump(self):
        with open(self._path, 'wb') as file_:
            pickle.dump(self._states, file_, pickle.HIGHEST_PROTOCOL)

    def get(self, item, default=None):
        """return item from config or default."""
        return self.__getitem__(item) or default

    def save(self):
        """write configurations to file."""
        self._dump()


class Session(Sess):
    """Custom ``requests.Session`` object model."""

    def __init__(self, base_url, *args, **kwargs):
        self.base_url = base_url
        super(Session, self).__init__(*args, **kwargs)

    def resource(self, uri, method='GET', payload=None, params=None,
                 endpoint_version='/v1'):
        """Resource access helper."""
        url = f'{self.base_url}{endpoint_version}{uri}'
        response = self.request(method, url, params=params, json=payload)

        try:
            response.raise_for_status()
            data = response.json()
        except JSONDecodeError:
            # Handel endpoints with none json payload.
            data = {}
        except HTTPError:
            if response.status_code == 400:
                if response.headers.get('Content-Type') == 'application/json':
                    error_msg = response.json()
                    if 'namespace_header' in error_msg:
                        selected_ns = response.request.headers.get("Digicloud-Namespace")
                        if selected_ns is None:
                            raise Exception("You need to select a namespace using "
                                            "'digicloud namespace select'")
                        else:
                            raise Exception(
                                "You've chosen an invalid namespace, "
                                "either you removed the current namespace, "
                                "left from it or "
                                "someone removed you.\n"
                                "You need to select one of your namespaces using "
                                "'digicloud namespace select'.\n"
                                "Also you can see list of your namespaces using "
                                "'digicloud namespace list'"
                            )
                    if 'region_header' in error_msg:
                        raise Exception("You need to select a region appropriately, "
                                        "by using 'digicloud region select' and "
                                        "'digicloud region list'")
            if response.status_code == 401 and not response.url.endswith('tokens'):
                error_msg = 'digicloud: Must login.'
            elif response.headers.get('Content-Type') == 'application/json':
                error_msg = yaml.safe_dump(response.json())
            else:
                error_msg = f'digicloud: {response.reason}({response.status_code})'
            raise Exception(error_msg)

        return data

    def get(self, uri, params=None):
        return self.resource(uri, params=params)

    def post(self, uri, payload):
        return self.resource(uri, 'POST', payload)

    def put(self, uri, payload):
        return self.resource(uri, 'PUT', payload)

    def patch(self, uri, payload):
        return self.resource(uri, 'PATCH', payload)

    def delete(self, uri, payload=None):
        return self.resource(uri, 'DELETE', payload)
