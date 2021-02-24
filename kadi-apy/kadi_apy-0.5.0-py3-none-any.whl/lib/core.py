# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import configparser
import os
import time

import requests
import urllib3

from kadi_apy.cli.lib.collections import CLICollection
from kadi_apy.cli.lib.groups import CLIGroup
from kadi_apy.cli.lib.miscellaneous import CLIMiscellaneous
from kadi_apy.cli.lib.miscellaneous import Miscellaneous
from kadi_apy.cli.lib.records import CLIRecord
from kadi_apy.cli.lib.templates import CLITemplate
from kadi_apy.cli.lib.users import CLIUser
from kadi_apy.cli.search import CLISearchResource
from kadi_apy.cli.search import CLISearchUser
from kadi_apy.globals import config_path
from kadi_apy.lib.exceptions import KadiAPYConfigurationError
from kadi_apy.lib.exceptions import KadiAPYRequestError
from kadi_apy.lib.resources.collections import Collection
from kadi_apy.lib.resources.groups import Group
from kadi_apy.lib.resources.records import Record
from kadi_apy.lib.resources.templates import Template
from kadi_apy.lib.resources.users import User
from kadi_apy.lib.search import SearchResource
from kadi_apy.lib.search import SearchUser


def _key_exit(key, instance):
    raise KadiAPYConfigurationError(
        f"Please define the key '{key}' for instance '{instance}' in the config file."
    )


def _read_config(config, value, instance):
    try:
        value_read = config[instance][value]
    except:
        _key_exit(value, instance)
    if not value_read:
        _key_exit(value, instance)
    return value_read


def _read_verify(config, instance):
    try:
        return config[instance].getboolean("verify")
    except ValueError:
        raise KadiAPYConfigurationError(
            "Please set either 'True' or 'False' in the config file for the"
            " key 'verify'."
        )


def _read_timeout(config, instance):
    try:
        return config[instance].getint("timeout")
    except ValueError:
        raise KadiAPYConfigurationError(
            "Please set an integer in the config file for the key 'timeout'."
        )


class KadiManager:
    r"""Base manager class for the API.

    Manages the host and the personal access token (PAT) to use for all API requests.

    :param instance: (optional) The name of the instance to use in combination with a
        config file.
    :param host: (optional) Name of the host.
    :param token: (optional) Personal access token.
    :param verify: (optional) Whether to verify the SSL/TLS certificate of the host.
    :param timeout: (optional) Timeout in seconds for the request.
    """

    def __init__(self, instance=None, host=None, token=None, verify=True, timeout=60):
        self.host = host
        self.token = token
        self.verify = verify
        self.timeout = timeout
        self._pat_user_id = None

        if host is None and token is None:
            if not os.path.exists(config_path):
                raise KadiAPYConfigurationError(
                    f"Config file does not exit at '{config_path}'.\n"
                    "You can run 'kadi-apy config create' to create the config file at"
                    f" '{config_path}."
                )

            config = configparser.ConfigParser()
            config.read(config_path)

            if instance is None:
                try:
                    instance = config["global"]["default"]
                except:
                    raise KadiAPYConfigurationError(
                        "No default instance defined in the config file at"
                        f" '{config_path}."
                    )

            instances = config.sections()
            instances.remove("global")

            if instance not in instances:
                raise KadiAPYConfigurationError(
                    "Please use an instance which is defined in the config file.\n"
                    f"Choose one of {instances}"
                )

            self.token = _read_config(config, "pat", instance)
            self.host = _read_config(config, "host", instance)

            if "verify" in config[instance]:
                self.verify = _read_verify(config, instance)
            elif "verify" in config["global"]:
                self.verify = _read_verify(config, "global")

            if "timeout" in config[instance]:
                self.timeout = _read_timeout(config, instance)
            elif "timeout" in config["global"]:
                self.timeout = _read_timeout(config, "global")

        if self.host is None:
            raise KadiAPYConfigurationError("No host information provided.")

        if self.token is None:
            raise KadiAPYConfigurationError("No personal access token (PAT) provided.")

        if self.host.endswith("/"):
            self.host = self.host[:-1]

        if not self.host.endswith("/api"):
            self.host = self.host + "/api"

        self.verify = verify
        if not self.verify:
            requests.packages.urllib3.disable_warnings(
                urllib3.exceptions.InsecureRequestWarning
            )

        self.misc = Miscellaneous(self)
        self.cli_misc = CLIMiscellaneous(self)

    def _make_request(self, endpoint, method=None, headers=None, timeout=1, **kwargs):
        if not endpoint.startswith(self.host):
            endpoint = self.host + endpoint

        response = getattr(requests, method)(
            endpoint,
            headers={"Authorization": f"Bearer {self.token}"},
            verify=self.verify,
            timeout=self.timeout,
            **kwargs,
        )

        # Check if any rate limit is exceeded and just wait an increasing amount of time
        # before repeating the request.
        if (
            response.status_code == 429
            and "Rate limit exceeded" in response.json()["description"]
        ):
            time.sleep(timeout)
            return self._make_request(
                endpoint, method=method, headers=headers, timeout=timeout + 1, **kwargs
            )

        return response

    def _get(self, endpoint, **kwargs):
        return self._make_request(endpoint, method="get", **kwargs)

    def _post(self, endpoint, **kwargs):
        return self._make_request(endpoint, method="post", **kwargs)

    def _patch(self, endpoint, **kwargs):
        return self._make_request(endpoint, method="patch", **kwargs)

    def _put(self, endpoint, **kwargs):
        return self._make_request(endpoint, method="put", **kwargs)

    def _delete(self, endpoint, **kwargs):
        return self._make_request(endpoint, method="delete", **kwargs)

    @property
    def pat_user_id(self):
        """Get the user id related to the PAT.

        :return: The user id.
        """

        if self._pat_user_id is None:
            response = self._get("/users/me")
            payload = response.json()
            if response.status_code == 200:
                self._pat_user_id = payload["id"]
            else:
                raise KadiAPYRequestError(payload)

        return self._pat_user_id

    def record(self, **kwargs):
        """Init a record"""

        return Record(manager=self, **kwargs)

    def collection(self, **kwargs):
        """Init a collection"""

        return Collection(manager=self, **kwargs)

    def group(self, **kwargs):
        """Init a collection"""

        return Group(manager=self, **kwargs)

    def user(self, **kwargs):
        """Init a user"""

        return User(manager=self, **kwargs)

    def template(self, **kwargs):
        """Init a template"""

        return Template(manager=self, **kwargs)

    def search_resource(self, **kwargs):
        """Init a search for resources"""

        return SearchResource(manager=self, **kwargs)

    def search_user(self, **kwargs):
        """Init a search for users"""

        return SearchUser(manager=self, **kwargs)

    def cli_record(self, **kwargs):
        """Init a record to be used in a cli"""

        return CLIRecord(manager=self, **kwargs)

    def cli_collection(self, **kwargs):
        """Init a collection to be used in a cli"""

        return CLICollection(manager=self, **kwargs)

    def cli_group(self, **kwargs):
        """Init a group to be used in a cli"""

        return CLIGroup(manager=self, **kwargs)

    def cli_user(self, **kwargs):
        """Init a user to be used in a cli"""

        return CLIUser(manager=self, **kwargs)

    def cli_template(self, **kwargs):
        """Init a template to be used in a cli"""

        return CLITemplate(manager=self, **kwargs)

    def cli_search_resource(self, **kwargs):
        """Init a search to be used for resources in a cli"""

        return CLISearchResource(manager=self, **kwargs)

    def cli_search_user(self, **kwargs):
        """Init a search to be used for users in a cli"""

        return CLISearchUser(manager=self, **kwargs)
