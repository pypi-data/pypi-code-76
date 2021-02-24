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


class Resource(ResourceMeta):
    r"""Generic model to represent different resources.

    :param id: (optional) The ID of an existing resource.
    :param identifier: (optional) The unique identifier of a new or existing resource,
        which is only relevant if no ID was given. If present, the identifier will be
        used to check for an existing resource instead. If no existing resource could be
        found or the resource to check does not use a unique identifier, it will be used
        to create a new resource instead, together with the additional metadata.
    :param \**kwargs: Additional metadata of the new resource to create.
    """

    name = "resource"

    def __init__(self, manager, id=None, identifier=None, create=False, **kwargs):
        super().__init__(manager)
        self.id = id
        self.created = False

        # If an ID was given, check if we can access the corresponding resource.
        if self.id is not None:
            response = self._get(f"{self.base_path}/{self.id}")
            if response.status_code != 200:
                raise KadiAPYRequestError(
                    f"Could not access the {self.name} with ID {self.id}."
                    f" {response.json()['description']}"
                )

            self._meta = response.json()

        # If an identifier was given, check if a resource already exists with the
        # same identifier.
        elif identifier is not None:
            response = self._get(f"{self.base_path}/identifier/{identifier}")

            # The identifier already exists, get the ID of the resource.
            if response.status_code == 200:
                self._meta = response.json()
                self.id = self._meta["id"]

            # The identifier already exists but we cannot access it.
            elif response.status_code == 403:
                raise KadiAPYRequestError(
                    f"The identifier '{identifier}' is already in use and you have no"
                    " access to the resource."
                )

            # Else, check if the identifier does not exist or if the resource even
            # uses unique identifiers, which we assume to be the case if the
            # "/identifier" endpoint is present.
            elif response.status_code != 404:
                raise KadiAPYRequestError(response.json())

            # If we still do not have an ID, we try to create the resource now.
            if self.id is None and create == True:
                payload = kwargs
                payload["identifier"] = identifier

                # Identifier is used as default title.
                if "title" not in payload or payload["title"] is None:
                    payload["title"] = identifier

                response = self._post(self.base_path, json=payload)

                if response.status_code != 201:
                    raise KadiAPYRequestError(response.json())

                self._meta = response.json()
                self.id = self._meta["id"]
                self.created = True

        else:
            raise KadiAPYInputError("No id or identifier given.")

        # If no id and no existing identifier is given and the flag create is False,
        # then we raise this exception.
        if self.id is None:
            raise KadiAPYInputError(
                f"The {self.name} with identifier '{identifier}' is not "
                f"present. You have to create it first."
            )

        # Save any related actions and links for future use, as these won't change
        # between requests.
        self._actions = self._meta["_actions"]
        self._links = self._meta["_links"]

        # Save the time the metadata was updated last.
        self._last_update = datetime.utcnow()

    def __str__(self):
        return (
            f"{self.name} '{self.meta['title']}' (id: {self.id}, identifier:"
            f" '{self.meta['identifier']}')"
        )

    def edit(self, **kwargs):
        r"""Edit the metadata of the resource.

        :param \**kwargs: The updated metadata of the resource.
        :return: The response object.
        """
        return self._patch(self._actions["edit"], json=kwargs)

    def delete(self):
        """Delete the resource.

        :return: The response object.
        """
        return self._delete(self._actions["delete"])
