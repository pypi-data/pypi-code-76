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
import fnmatch
import json
import os
import pathlib
import sys

import click

from kadi_apy.cli.commons import item_add_collection_link
from kadi_apy.cli.commons import item_add_group_role
from kadi_apy.cli.commons import item_add_tag
from kadi_apy.cli.commons import item_add_user
from kadi_apy.cli.commons import item_delete
from kadi_apy.cli.commons import item_print_info
from kadi_apy.cli.commons import item_remove_collection_link
from kadi_apy.cli.commons import item_remove_group_role
from kadi_apy.cli.commons import item_remove_tag
from kadi_apy.cli.commons import item_remove_user
from kadi_apy.cli.commons import item_set_attribute
from kadi_apy.cli.commons import print_item_created
from kadi_apy.cli.commons import raise_request_error
from kadi_apy.lib.exceptions import KadiAPYInputError
from kadi_apy.lib.resources.records import Record


def _upload(self, file_path, replace=False):
    """Prepare uploading files."""

    file_name = file_path.split(os.sep)[-1]

    click.echo(f"Prepare upload of file '{file_name}'")

    response = super(self.__class__, self).upload_file(
        file_path=file_path, replace=replace
    )
    if response.status_code == 409 and not replace:
        click.echo(
            f"A file with the name '{file_name}' already exists.\nFile '{file_name}' "
            "was not uploaded. Use '-f' to force overwriting existing file."
        )
    elif response.status_code == 200:
        click.echo(f"Upload of file '{file_name}' was successful.")
    else:
        click.echo(f"Upload of file '{file_name}' was not successful. ")
        raise_request_error(response=response)


def _rename_duplicate_entry(filepath_store, index):
    path = pathlib.Path(filepath_store)
    base = ""
    if len(path.parts) > 1:
        base = os.path.join(*path.parts[:-1])
    file_name = f"{path.stem}_{index}{path.suffix}"
    return os.path.join(base, file_name)


class CLIRecord(Record):
    """Records class to be used in a cli."""

    def __init__(self, pipe=False, title=None, create=False, **kwargs):
        super().__init__(title=title, create=create, **kwargs)

        print_item_created(self, title=title, pipe=pipe, create=create)

    def set_attribute(self, **kwargs):
        # pylint: disable=arguments-differ
        return item_set_attribute(self, **kwargs)

    def add_user(self, user, permission_new):
        # pylint: disable=arguments-differ
        return item_add_user(self, user=user, permission_new=permission_new)

    def add_group_role(self, group, permission_new):
        # pylint: disable=arguments-differ
        return item_add_group_role(self, group=group, permission_new=permission_new)

    def remove_group_role(self, group):
        # pylint: disable=arguments-differ
        return item_remove_group_role(self, group=group)

    def print_info(self, **kwargs):
        """Print record infos."""

        return item_print_info(self, **kwargs)

    def upload_file(self, file_name, pattern, force):
        # pylint: disable=arguments-differ
        """Upload files into a record."""

        if not os.path.isdir(file_name):
            if not os.path.isfile(file_name):
                raise KadiAPYInputError(f"File: {file_name} does not exist.")

            _upload(self, file_path=file_name, replace=force)

        else:
            path_folder = file_name
            filelist = fnmatch.filter(os.listdir(path_folder), pattern)

            if not filelist:
                click.echo("Found no file to upload.")
                sys.exit(0)

            for file_upload in filelist:
                file_path = os.path.join(path_folder, file_upload)

                if os.path.isdir(file_path):
                    continue

                _upload(self, file_path=file_path, replace=force)

    def remove_user(self, user):
        # pylint: disable=arguments-differ
        return item_remove_user(self, user=user)

    def delete(self, i_am_sure):
        # pylint: disable=arguments-differ
        return item_delete(self, i_am_sure=i_am_sure)

    def add_metadatum(self, metadatum_new, force):
        """Add a metadatum to a record."""
        # pylint: disable=arguments-differ

        metadatum = metadatum_new["key"]
        unit = metadatum_new["unit"]
        value = metadatum_new["value"]

        if force is False and super().check_metadatum(metadatum):
            raise KadiAPYInputError(
                f"Metadatum '{metadatum}' already exists. Use '--force' to overwrite "
                "it or change the name."
            )

        metadata_before_update = self.meta["extras"]

        response = super().add_metadatum(metadatum_new, force)

        metadata_after_update = self.meta["extras"]

        if response.status_code == 200:
            if metadata_before_update == metadata_after_update:
                click.echo(f"Metadata were not changed.")
            else:
                text_unit = ""
                if unit is not None:
                    text_unit = f"and the unit '{unit}' "
                click.echo(
                    f"Successfully added metadatum '{metadatum}' with the value "
                    f"'{value}' {text_unit}to {self}."
                )
        else:
            click.echo(
                f"Something went wrong when trying to add new metadatum '{metadatum}'"
                f" to {self}."
            )
            raise_request_error(response=response)

    def add_metadata(self, metadata=None, file=None, force=False):
        """Add metadata with dict or a list of dicts as input."""
        # pylint: disable=arguments-differ

        if (metadata is None and file is None) or (
            metadata is not None and file is not None
        ):
            raise KadiAPYInputError("Please specify either metadata or a file.")

        if file and not os.path.isfile(file):
            raise KadiAPYInputError(f"File: '{file}' does not exist.")

        try:
            if file:
                with open(file, encoding="utf-8") as f:
                    metadata = json.load(f)
            elif isinstance(metadata, list):
                pass
            else:
                metadata = json.loads(metadata)
        except json.JSONDecodeError as e:
            raise KadiAPYInputError(f"Error loading JSON input ({e}).")

        def _callback(metadatum, is_nested):
            if is_nested:
                click.echo(
                    f"Metadatum {metadatum['key']} is of type '{metadatum['type']}' and"
                    " will not be replaced."
                )
            else:
                metadatum_key = metadatum["key"]
                try:
                    metadatum_unit = metadatum["unit"]
                except:
                    metadatum_unit = None
                metadatum_value = metadatum["value"]

                text_unit = ""
                if metadatum_unit is not None:
                    text_unit = f"and the unit '{metadatum_unit}' "
                click.echo(
                    f"Found metadatum '{metadatum_key}' with the value "
                    f"'{metadatum_value}' {text_unit}to add to {self}."
                )

        metadata_before_update = self.meta["extras"]

        response = super().add_metadata(metadata, force, callback=_callback)

        metadata_after_update = self.meta["extras"]

        if response.status_code == 200:
            if metadata_before_update == metadata_after_update:
                click.echo(f"Metadata were not changed.")
            else:
                click.echo(f"Successfully updated the metadata of {self}.")
        else:
            click.echo(
                f"Something went wrong when trying to add new metadata to {self}."
            )
            raise_request_error(response=response)

    def get_file(self, filepath, force, file_id=None):
        """Download one file or all files from a record."""
        # pylint: disable=arguments-differ

        list_file_ids = []
        list_file_names = []

        if file_id is not None:
            try:
                list_file_names.append(super().get_file_name(file_id))
            except KadiAPYInputError as e:
                click.echo(e, err=True)
                sys.exit(1)

            list_file_ids.append(file_id)

        else:
            page = 1
            response = super().get_filelist(page=page, per_page=100)

            if response.status_code == 200:
                payload = response.json()
                total_pages = payload["_pagination"]["total_pages"]
                for page in range(1, total_pages + 1):
                    if page != 1:
                        response = super().get_filelist(page=page, per_page=100)
                        payload = response.json()

                    for results in payload["items"]:
                        list_file_ids.append(results["id"])
                        list_file_names.append(results["name"])
            else:
                raise_request_error(response=response)

            number_files = len(list_file_ids)
            if number_files == 0:
                click.echo(f"No files present in {self}.")
                return

            click.echo(f"Starting to download {number_files} file(s) from {self}.")

        list_downloaded = []

        for name_iter, id_iter in zip(list_file_names, list_file_ids):
            filepath_store = os.path.join(filepath, name_iter)
            index = 2
            filepath_temp = filepath_store

            if force:
                while filepath_temp in list_downloaded:
                    filepath_temp = _rename_duplicate_entry(filepath_store, index)
                    index += 1

                list_downloaded.append(filepath_temp)

            else:
                while os.path.isfile(filepath_temp):
                    filepath_temp = _rename_duplicate_entry(filepath_store, index)
                    index += 1

            response = super().download_file(id_iter, filepath_temp)

            if response.status_code == 200:
                click.echo(
                    f"Successfully downloaded file '{name_iter}' from {self} and "
                    f"stored in {filepath_temp}."
                )
            else:
                click.echo(
                    f"Something went wrong when trying to download file '{name_iter}' "
                    f"from {self}."
                )
                raise_request_error(response=response)

    def add_tag(self, tag):
        return item_add_tag(self, tag)

    def remove_tag(self, tag):
        return item_remove_tag(self, tag)

    def link_record(self, record_to, name):
        """Add a record link to a record."""

        response = super().get_record_links(page=1, per_page=100)

        if response.status_code == 200:
            payload = response.json()
            total_pages = payload["_pagination"]["total_pages"]
            for page in range(1, total_pages + 1):
                for results in payload["items"]:
                    if (
                        results["record_to"]["id"] == record_to.id
                        and results["name"] == name
                    ):
                        click.echo(f"Link already exsists. Nothing to do.")
                        return
                if page < total_pages:
                    response = super().get_record_links(page=page + 1, per_page=100)
                    if response.status_code == 200:
                        payload = response.json()
                    else:
                        raise_request_error(response)
            response = super().link_record(record_to=record_to.id, name=name)
            if response.status_code == 201:
                click.echo(f"Successfully linked {self} to {str(record_to)}.")
            else:
                raise_request_error(response=response)
        else:
            raise_request_error(response)

    def delete_record_link(self, record_link_id):
        """Delete a record link."""

        response = super().delete_record_link(record_link_id=record_link_id)
        if response.status_code == 204:
            click.echo(
                f"Linking of record {self.id} with link id {record_link_id} was "
                "deleted."
            )
        else:
            raise_request_error(response=response)

    def get_record_links(self, page, per_page, direction):
        """Print record links to another record."""
        # pylint: disable=arguments-differ

        response = super().get_record_links(
            page=page, per_page=per_page, direction=direction
        )
        if response.status_code == 200:
            payload = response.json()
            click.echo(
                f"Found {payload['_pagination']['total_items']} record(s) on "
                f"{payload['_pagination']['total_pages']} page(s).\n"
                f"Showing results of page {page}:"
            )
            record_direction = f"record_{direction}"
            for results in payload["items"]:
                click.echo(
                    f"Link id {results['id']}: Link name: '{results['name']}'. Record "
                    f"{self.id} is linked {direction} record "
                    f"{results[record_direction]['id']} with the title "
                    f"'{results[record_direction]['title']}'."
                )
        else:
            raise_request_error(response=response)

    def get_metadatum(self, name, information, pipe):
        """Print a information of a metadatum."""

        found = False
        for obj in self.meta["extras"]:
            if obj["key"] == name:
                found = True
                try:
                    content = obj[information]
                    if not pipe:
                        return click.echo(
                            f"The metadatum '{name}' has the {information} '{content}'."
                        )

                    return click.echo(content)
                except:
                    click.echo(f"Metadatum '{name}' has no {information}.")

        if found == False:
            click.echo(f"Metadatum '{name}' is not present in {self}.")

    def edit_file(self, file, name, mimetype):
        """Edit the metadata of a file of a record."""
        # pylint: disable=arguments-differ

        if name is not None and self.has_file(name):
            click.echo(f"File {name} already present in {self}.")
            sys.exit(1)

        response = super().edit_file(file, name=name, mimetype=mimetype)
        if response.status_code != 200:
            raise_request_error(response)
        else:
            click.echo("File updated successfully.")

    def delete_file(self, file_id):
        """Delete a file of a record."""
        # pylint: disable=arguments-differ

        response = super().delete_file(file_id)
        if response.status_code != 204:
            raise_request_error(response)
        else:
            click.echo("File deleted successfully.")

    def delete_files(self, i_am_sure):
        """Delete all files of a record."""

        if not i_am_sure:
            raise KadiAPYInputError(
                f"If you are sure you want to delete all files in {self}, "
                "use the flag --i-am-sure."
            )

        response = super().get_filelist(page=1, per_page=100)

        if response.status_code == 200:
            payload = response.json()
            total_pages = payload["_pagination"]["total_pages"]
            for page in range(1, total_pages + 1):
                for results in payload["items"]:
                    response_delete = super().delete_file(results["id"])
                    if response_delete.status_code != 204:
                        raise_request_error(response_delete)
                    else:
                        click.echo(f"Deleting file {results['name']} was successful.")
                if page < total_pages:
                    response = super().get_filelist(page=1, per_page=100)
                    if response.status_code == 200:
                        payload = response.json()
                    else:
                        raise_request_error(response)

        else:
            raise_request_error(response)

    def remove_metadatum(self, metadatum):
        """Delete a metadatum of a record."""

        if super().check_metadatum(metadatum):
            response = super().remove_metadatum(metadatum)
            if response.status_code == 200:
                click.echo(f"Successfully removed metadatum '{metadatum}' from {self}.")
            else:
                click.echo(
                    f"Something went wrong when trying to remove metadatum "
                    f"'{metadatum}' from {self}."
                )
                raise_request_error(response=response)
        else:
            click.echo(
                f"Metadatum '{metadatum}' is not present in {self}. Nothing to do."
            )

    def remove_all_metadata(self, i_am_sure=False):
        # pylint: disable=arguments-differ
        if not i_am_sure:
            raise KadiAPYInputError(
                f"If you are sure you want to delete all metadata in {self}, "
                "use the flag --i-am-sure."
            )

        response = super().remove_all_metadata()
        if response.status_code == 200:
            click.echo(f"Successfully removed all metadata from {self}.")
        else:
            raise_request_error(response)

    def add_collection_link(self, collection):
        """Add collection link to record."""
        # pylint: disable=arguments-differ

        return item_add_collection_link(self, collection)

    def remove_collection_link(self, collection):
        """Add collection link to record."""
        # pylint: disable=arguments-differ

        return item_remove_collection_link(self, collection)
