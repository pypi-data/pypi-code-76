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
from datetime import datetime

from kadi_apy.lib.exceptions import KadiAPYInputError
from kadi_apy.lib.exceptions import KadiAPYRequestError
from kadi_apy.lib.helper import ResourceMeta


class User(ResourceMeta):
    """Model to represent users."""

    base_path = "/users"
    name = "user"

    def __init__(self, manager, id=None, username=None, identity_type=None, **kwargs):
        super().__init__(manager)
        self.id = id
        self._meta = None

        if self.id is not None:
            response = self._get(f"{self.base_path}/{self.id}")
            if response.status_code != 200:
                raise KadiAPYRequestError(
                    f"The user with ID {self.id} does not exist.\n"
                    f"{response.json()['description']}"
                )

            self._meta = response.json()

        elif username is not None and identity_type is not None:
            response = self._get(f"{self.base_path}/{identity_type}/{username}")
            if response.status_code != 200:
                raise KadiAPYRequestError(
                    f"The user with username {username} and identity type "
                    f"{identity_type} does not exist.\n{response.json()['description']}"
                )
            self._meta = response.json()
            self.id = self._meta["id"]

        else:
            raise KadiAPYInputError(
                f"Please specify the user via id or username and identity type."
            )

        # Save the time the metadata was updated last.
        self._last_update = datetime.utcnow()

    def __str__(self):
        return (
            f"{self.meta['identity']['identity_name']} account "
            f"'{self.meta['identity']['displayname']}' (id: {self.id}, username:  "
            f"{self.meta['identity']['username']})"
        )
