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
import copy
import os
import time
from io import BytesIO

from kadi_apy.lib import commons
from kadi_apy.lib.exceptions import KadiAPYInputError
from kadi_apy.lib.exceptions import KadiAPYRequestError
from kadi_apy.lib.resource import Resource


def _remove_key(list, key_remove):
    return [obj for obj in list if obj["key"] != key_remove]


class Record(Resource):
    """Model to represent records."""

    base_path = "/records"
    name = "record"

    def add_user(self, user_id, role_name):
        """Add a user."""

        return commons.add_user(self, user_id, role_name)

    def remove_user(self, user_id):
        """Remove a user."""

        return commons.remove_user(self, user_id)

    def add_group_role(self, group_id, role_name):
        """Add a group role to a record."""

        return commons.add_group_role(self, group_id, role_name)

    def remove_group_role(self, group_id):
        """Remove a group role from a record."""

        return commons.remove_group_role(self, group_id)

    def add_collection_link(self, collection_id):
        """Add a record to a collection."""

        return commons.add_collection_link(self, collection_id)

    def remove_collection_link(self, collection_id):
        """Remove a record from a collection."""

        return commons.remove_collection_link(self, collection_id)

    def check_metadatum(self, metadatum):
        """Check if a record has a certain metadatum."""

        for obj in self.meta["extras"]:
            if obj["key"] == metadatum:
                return True
        return False

    def add_metadatum(self, metadatum, force=False):
        """Add metadatum to a record."""

        endpoint = self._actions["edit"]
        metadata = copy.deepcopy(self.meta["extras"])

        if self.check_metadatum(metadatum["key"]):
            if force:
                metadata = [obj for obj in metadata if obj["key"] != metadatum["key"]]
                metadata.append(metadatum)
        else:
            metadata.append(metadatum)

        return self._patch(endpoint, json={"extras": metadata})

    def add_metadata(self, metadata_new, force=False, print=False, callback=None):
        r"""Add metadata to a record.

        :param metadata_new: One or more metadata entries to add, either as dictionary
            or a list of dictionaries.
        """
        # TODO validation does not work for nested metadata

        if not isinstance(metadata_new, list):
            metadata_new = [metadata_new]

        metadata_old = copy.deepcopy(self.meta["extras"])

        for metadatum_new in metadata_new:
            found = False
            for metadatum_old in metadata_old:
                if metadatum_new["key"] == metadatum_old["key"]:
                    found = True
                    if force:
                        if metadatum_old["type"] in ["dict", "list"]:
                            metadata_new = _remove_key(
                                metadata_new, metadatum_old["key"]
                            )
                            if callback:
                                callback(metadatum_old, True)
                        else:
                            metadata_old = _remove_key(
                                metadata_old, metadatum_old["key"]
                            )
                            if callback:
                                callback(metadatum_new, False)
                    else:
                        metadata_new = _remove_key(metadata_new, metadatum_old["key"])

            if callback and not found:
                callback(metadatum_new, False)

        return self._patch(
            self._actions["edit"], json={"extras": metadata_old + metadata_new}
        )

    def remove_metadatum(self, metadatum):
        """Remove a metadatum from a record."""
        metadata = [obj for obj in self.meta["extras"] if obj["key"] != metadatum]
        return self._patch(self._actions["edit"], json={"extras": metadata})

    def remove_all_metadata(self):
        """Remove all metadata from a record."""
        return self._patch(self._actions["edit"], json={"extras": []})

    def _upload(self, f_size, obj, file_name, replace=False):
        endpoint = self._actions["new_upload"]

        # Prepare new file upload.
        response = self._post(endpoint, json={"name": file_name, "size": f_size})
        if response.status_code == 409 and replace:
            endpoint = response.json()["file"]["_actions"]["edit_data"]
            response = self._put(endpoint, json={"size": f_size})

        if response.status_code != 201:
            return response

        payload = response.json()

        endpoint = payload["_actions"]["upload_chunk"]
        chunk_count = payload["chunk_count"]
        chunk_size = payload["_meta"]["chunk_size"]

        for i in range(chunk_count):
            if i == chunk_count - 1:
                # Last chunk.
                chunk_size = f_size % chunk_size
            read_data = obj.read(chunk_size)
            files = {"blob": read_data}
            data = {"index": i, "size": chunk_size}

            response_put = self._put(endpoint, files=files, data=data)
            if response_put.status_code != 200:
                return response_put

        # Finish upload.
        endpoint = payload["_actions"]["finish_upload"]

        response_post = self._post(endpoint)
        if response_post.status_code != 202:
            return response_post

        endpoint = payload["_links"]["status"]
        while True:
            response_get = self._get(endpoint)
            if response_get.status_code == 200:
                data = response_get.json()
                if data["state"] in ["active", "inactive"]:
                    break
            # TODO: increase time and break loop if something goes wrong.
            time.sleep(2)
        return response_get

    def upload_file(self, file_path, file_name=None, replace=False):
        """Upload a file into a record."""
        if file_name is None:
            file_name = file_path.split(os.sep)[-1]

        with open(file_path, "rb") as f:
            f_size = os.fstat(f.fileno()).st_size

            return self._upload(
                f_size=f_size, obj=f, file_name=file_name, replace=replace
            )

    def upload_string_to_file(self, string, file_name):
        """Upload a string to save as a file a record."""

        mem = BytesIO()
        data = string.encode()
        f_size = len(data)
        mem.write(data)
        mem.seek(0)

        return self._upload(f_size=f_size, obj=mem, file_name=file_name)

    def download_file(self, file_id, file_path):
        """Download a file from a record."""

        endpoint = f"{self.base_path}/{self.id}/files/{file_id}/download"

        response = self._get(endpoint, stream=True)
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return response

    def get_users(self, **params):
        """Get users from a record. Supports pagination."""

        endpoint = f"{self.base_path}/{self.id}/roles/users"
        return self._get(endpoint, params=params)

    def change_user_role(self, user_id, role_name):
        """Change user role."""

        endpoint = f"{self.base_path}/{self.id}/roles/users/{user_id}"
        data = {"name": role_name}
        return self._patch(endpoint, json=data)

    def change_group_role(self, group_id, role_name):
        """Change group role."""

        return commons.change_group_role(self, group_id, role_name)

    def get_filelist(self, **params):
        """Get the filelist."""

        endpoint = f"{self.base_path}/{self.id}/files"
        return self._get(endpoint, params=params)

    def get_number_files(self):
        """Get number of all files of a record."""

        response = self.get_filelist()
        if response.status_code == 200:
            payload = response.json()
            return payload["_pagination"]["total_items"]
        raise KadiAPYRequestError(response.json())

    def get_file_name(self, file_id):
        """Get file name from a given file ID."""

        endpoint = f"{self.base_path}/{self.id}/files/{file_id}"
        response = self._get(endpoint)
        if response.status_code == 200:
            return response.json()["name"]

        raise KadiAPYInputError(f"No file with id {file_id} in record {self.id}.")

    def add_tag(self, tag):
        """Add a tag."""

        return commons.add_tag(self, tag.lower())

    def remove_tag(self, tag):
        """Remove a tag."""

        return commons.remove_tag(self, tag)

    def get_tags(self):
        """Get all tags."""

        return commons.get_tags(self)

    def check_tag(self, tag):
        """Check if given tag is already present."""

        return commons.check_tag(self, tag)

    def set_attribute(self, attribute, value):
        """Set attribute."""

        return commons.set_attribute(self, attribute, value)

    def link_record(self, record_to, name):
        """Link record."""

        endpoint = self._actions["link_record"]
        data = {"record_to": {"id": record_to}, "name": name}
        return self._post(endpoint, json=data)

    def delete_record_link(self, record_link_id):
        """Delete a record link."""

        # attention: record_link_id is not linked record id
        return self._delete(f"{self.base_path}/{self.id}/records/{record_link_id}")

    def get_record_links(self, **params):
        """Get record links."""

        endpoint = f"{self.base_path}/{self.id}/records"
        return self._get(endpoint, params=params)

    def get_file_id(self, file_name):
        """Get the file id."""

        response = self._get(f"{self.base_path}/{self.id}/files/name/{file_name}")

        if response.status_code == 200:
            return response.json()["id"]

        raise KadiAPYInputError(f"No file with name {file_name} in record {self.id}.")

    def has_file(self, file_name):
        """Check if file with given name already exists."""

        try:
            self.get_file_id(file_name)
            return True
        except:
            return False

    def edit_file(self, file_id, **kwargs):
        r"""Edit the metadata of a file of the record.

        :param file_id: The ID (UUID) of the file to edit.
        :param \**kwargs: The metadata to update the file with.
        """
        kwargs = {key: value for key, value in kwargs.items() if value is not None}

        return self._patch(f"{self.base_path}/{self.id}/files/{file_id}", json=kwargs)

    def delete_file(self, file_id):
        r"""Delete a file of the record.

        :param file_id: The ID (UUID) of the file to delete.
        """
        return self._delete(f"{self.base_path}/{self.id}/files/{file_id}")
