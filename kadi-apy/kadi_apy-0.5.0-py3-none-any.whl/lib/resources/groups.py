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
from kadi_apy.lib import commons
from kadi_apy.lib.resource import Resource


class Group(Resource):
    """Model to represent groups."""

    base_path = "/groups"
    name = "group"

    def add_user(self, user_id, role_name):
        """Add a user."""

        endpoint = self._actions["add_member"]
        data = {"role": {"name": role_name}, "user": {"id": user_id}}
        return self._post(endpoint, json=data)

    def remove_user(self, user_id):
        """Remove a user."""

        endpoint = f"{self.base_path}/{self.id}/members/{user_id}"
        return self._delete(endpoint, json=None)

    def change_user_role(self, user_id, role_name):
        """Change role of a user."""

        endpoint = f"{self._actions['add_member']}/{user_id}"
        data = {"name": role_name}
        return self._patch(endpoint, json=data)

    def add_collection(self, collection_id):
        """Add a collection."""

        return commons.add_collection(self, collection_id)

    def remove_collection(self, collection_id):
        """Remove a collection."""

        return commons.remove_collection(self, collection_id)

    def add_record(self, record_id):
        """Add a record."""

        return commons.add_record(self, record_id)

    def remove_record(self, record_id):
        """Remove a record."""

        return commons.remove_record(self, record_id)

    def get_records(self, **params):
        """Get records of a group. Supports pagination."""

        endpoint = f"{self.base_path}/{self.id}/records"
        return self._get(endpoint, params=params)

    def get_users(self, **params):
        """Get users of a group. Supports pagination."""

        endpoint = f"{self.base_path}/{self.id}/members"
        return self._get(endpoint, params=params)

    def get_collections(self, **params):
        """Get collections of a group. Supports pagination."""

        endpoint = f"{self.base_path}/{self.id}/collections"
        return self._get(endpoint, params=params)

    def set_attribute(self, attribute, value):
        """Set attribute."""

        return commons.set_attribute(self, attribute, value)
