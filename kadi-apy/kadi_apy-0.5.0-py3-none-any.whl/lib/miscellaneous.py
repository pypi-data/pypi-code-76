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
from kadi_apy.lib.helper import RequestMixin


class Miscellaneous(RequestMixin):
    """Model to handle miscellaneous."""

    def get_deleted_resources(self, **params):
        """Get a list of deleted resources in the trash."""

        endpoint = "/trash"
        return self._get(endpoint, params=params)

    def restore(self, item, item_id):
        """Restore an item from the trash."""

        endpoint = f"{item.base_path}/{item_id}/restore"
        return self._post(endpoint)

    def purge(self, item, item_id):
        """Purge an item from the trash."""

        endpoint = f"{item.base_path}/{item_id}/purge"
        return self._post(endpoint)

    def get_licenses(self, **params):
        """Get a list of available licences."""

        endpoint = "/licenses"
        return self._get(endpoint, params=params)
