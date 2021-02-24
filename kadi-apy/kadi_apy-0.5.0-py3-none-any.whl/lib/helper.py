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
from datetime import timedelta

from kadi_apy.lib.exceptions import KadiAPYRequestError


class RequestMixin:
    """Helper function for managing an instance stored in manager."""

    def __init__(self, manager):
        self.manager = manager

    def _get(self, endpoint, **kwargs):
        return self.manager._get(endpoint, **kwargs)

    def _post(self, endpoint, **kwargs):
        return self.manager._post(endpoint, **kwargs)

    def _patch(self, endpoint, **kwargs):
        return self.manager._patch(endpoint, **kwargs)

    def _put(self, endpoint, **kwargs):
        return self.manager._put(endpoint, **kwargs)

    def _delete(self, endpoint, **kwargs):
        return self.manager._delete(endpoint, **kwargs)


class ResourceMeta(RequestMixin):
    """Helper functions."""

    @property
    def meta(self):
        """Get all metadata of the resource.

        In case the previous metadata was invalidated, either manually, after a timeout
        or due to another request, a request will be sent to retrieve the possibly
        updated metadata again.

        :return: The metadata of the resource.
        """

        # pylint: disable=access-member-before-definition

        # Invalidate the cached metadata automatically after 5 minutes.
        if (datetime.utcnow() - self._last_update) > timedelta(minutes=5):
            self.invalidate_meta()

        if self._meta is None:
            response = self._get(f"{self.base_path}/{self.id}")
            if response.status_code != 200:
                raise KadiAPYRequestError(response.json())

            self._meta = response.json()
            self._last_update = datetime.utcnow()

        return self._meta

    def invalidate_meta(self):
        """Explicitly invalidate the cached metadata of the resource."""
        self._meta = None

    def __getattribute__(self, attr):
        if attr in ["_patch", "_delete"]:
            self.invalidate_meta()

        return super().__getattribute__(attr)
