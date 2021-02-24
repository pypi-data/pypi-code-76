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
from xmlhelpy import Choice
from xmlhelpy import Integer
from xmlhelpy import IntRange
from xmlhelpy import option
from xmlhelpy import Path

from kadi_apy.cli.commons import validate_metadatum
from kadi_apy.cli.decorators import apy_command
from kadi_apy.cli.decorators import file_id_options
from kadi_apy.cli.decorators import id_identifier_options
from kadi_apy.cli.decorators import user_id_options
from kadi_apy.cli.main import kadi_apy


@kadi_apy.group()
def records():
    """Commands to manage records."""


@records.command()
@apy_command
@option(
    "identifier",
    char="i",
    required=True,
    description="Identifier of the record",
    default=None,
)
@option("title", char="t", description="Title of the record")
@option(
    "visibility",
    char="v",
    description="Visibility of the record",
    default="private",
    param_type=Choice(["private", "public"]),
)
@option(
    "pipe",
    char="p",
    description="Use this flag if you want to pipe the returned record id.",
    is_flag=True,
)
def create(manager, **kwargs):
    """Create a record."""

    manager.cli_record(create=True, **kwargs)


@records.command()
@apy_command
@id_identifier_options(class_type="cli_record", helptext="to edit")
@option(
    "visibility",
    char="v",
    description="Visibility of the record",
    default=None,
    param_type=Choice(["private", "public"]),
)
@option("title", char="t", default=None, description="Title of the record")
@option("description", char="d", default=None, description="Description of the record")
@option("type", char="y", default=None, description="Type of the record")
def edit(record, **kwargs):
    """Edit visibility, title or description of a record."""

    record.set_attribute(**kwargs)


@records.command()
@apy_command
@id_identifier_options(class_type="cli_record", keep_manager=True)
@user_id_options("to add")
@option(
    "permission-new",
    char="p",
    description="Permission of new user",
    default="member",
    param_type=Choice(["member", "editor", "admin"]),
)
def add_user(record, user, permission_new):
    """Add a user to a record."""

    record.add_user(user, permission_new)


@records.command()
@apy_command
@id_identifier_options(
    class_type="cli_record",
    helptext="to add the group with role permissions",
    keep_manager=True,
)
@id_identifier_options(class_type="group")
@option(
    "permission-new",
    char="p",
    description="Permission of the group",
    default="member",
    param_type=Choice(["member", "editor", "admin"]),
)
def add_group_role(record, group, permission_new):
    """Add a group role to a record."""

    record.add_group_role(group, permission_new)


@records.command()
@apy_command
@id_identifier_options(class_type="cli_record", keep_manager=True)
@id_identifier_options(class_type="group")
def remove_group_role(record, group):
    """Remove a group role from a record."""

    record.remove_group_role(group)


@records.command()
@apy_command
@id_identifier_options(class_type="cli_record")
@option(
    "description",
    char="d",
    description="Show the description of the record",
    is_flag=True,
    default=False,
)
@option(
    "filelist",
    char="l",
    description="Show the filelist of the record",
    is_flag=True,
    default=False,
)
@option(
    "page", char="p", description="Page for filelist", param_type=Integer, default=1
)
@option(
    "per-page",
    char="n",
    description="Number of results per page",
    param_type=IntRange(1, 100),
    default=10,
)
@option(
    "metadata",
    char="m",
    description="Show the metadata of the record",
    is_flag=True,
    default=False,
)
@option(
    "visibility",
    char="v",
    description="Show the visibility of the record",
    is_flag=True,
    default=False,
)
@option(
    "pipe",
    char="i",
    description="Use for piping. Do not show basic info.",
    is_flag=True,
    default=False,
)
def show_info(record, **kwargs):
    """Prints information of a record."""

    record.print_info(**kwargs)


@records.command()
@apy_command
@id_identifier_options(class_type="cli_record")
@option("file-name", char="n", required=True, description="Name of the file or folder")
@option(
    "pattern",
    char="p",
    description="Pattern for selecting certain files when using a folder as input, e.g."
    " '*.txt'.",
    default="*",
)
@option(
    "force",
    char="f",
    description="Enable if existing file(s) with identical name(s) should be replaced.",
    is_flag=True,
    default=False,
)
def add_files(record, **kwargs):
    """Add a file or a folder content to a record."""

    record.upload_file(**kwargs)


@records.command()
@apy_command
@id_identifier_options(class_type="cli_record", keep_manager=True)
@user_id_options(helptext="to remove")
def remove_user(record, user):
    """Remove a user from a record."""

    record.remove_user(user)


@records.command()
@apy_command
@id_identifier_options(class_type="cli_record", helptext="to delete")
@option(
    "i-am-sure", description="Enable this option to delete the record", is_flag=True
)
def delete(record, i_am_sure):
    """Delete a record."""

    record.delete(i_am_sure)


@records.command()
@apy_command
@id_identifier_options(class_type="cli_record", helptext="to add a metadatum")
@option("metadatum", char="m", required=True, description="Name of metadatum to add")
@option("value", char="v", required=True, description="Value of metadatum to add")
@option(
    "type",
    char="t",
    description="Type of metadatum to add",
    param_type=Choice(["string", "integer", "float", "boolean"]),
    default="string",
)
@option(
    "unit",
    char="u",
    description="Unit of metadatum to add",
    default=None,
)
@option(
    "force",
    char="f",
    description="Force overwriting existing metadatum with identical name",
    is_flag=True,
    default=False,
)
def add_metadatum(record, force, metadatum, value, type, unit):
    """Add a metadatum to a record."""

    metadatum_new = validate_metadatum(
        metadatum=metadatum, value=value, type=type, unit=unit
    )

    record.add_metadatum(metadatum_new=metadatum_new, force=force)


@records.command()
@apy_command
@id_identifier_options(
    class_type="cli_record",
    helptext="to add metadata as dictionary or as a list of dictionaries",
)
@option("metadata", char="m", description="Metadata string input", default=None)
@option(
    "file",
    char="p",
    description="Path to file containing metadata",
    param_type=Path(exists=True),
    default=None,
)
@option(
    "force",
    char="f",
    description="Force deleting and overwriting existing metadata",
    is_flag=True,
    default=False,
)
def add_metadata(record, metadata, file, force):
    """Add metadata with dict or a list of dicts as input."""

    record.add_metadata(metadata=metadata, file=file, force=force)


@records.command()
@apy_command
@id_identifier_options(class_type="cli_record", helptext="to delete a metadatum")
@option("metadatum", char="m", required=True, description="Name of metadatum to remove")
def delete_metadatum(record, metadatum):
    """Delete a metadatum of a record."""

    record.remove_metadatum(metadatum)


@records.command()
@apy_command
@id_identifier_options(class_type="cli_record", helptext="to delete all metadata")
@option(
    "i-am-sure",
    description="Enable this option to delete all metadata of the record",
    is_flag=True,
)
def delete_all_metadata(record, i_am_sure):
    """Delete all metadatum of a record."""

    record.remove_all_metadata(i_am_sure)


@records.command()
@apy_command
@id_identifier_options(class_type="cli_record", helptext="to download files from")
@file_id_options(helptext="to download", required=False)
@option(
    "filepath",
    char="p",
    description="Path (folder) to store the file",
    param_type=Path(exists=True),
    default=".",
)
@option(
    "force",
    char="f",
    description="Force overwriting file in the given folder",
    is_flag=True,
    default=False,
)
def get_file(record, file_id, filepath, force):
    """Download one file or all files from a record."""

    record.get_file(filepath, force, file_id)


@records.command()
@apy_command
@id_identifier_options(class_type="cli_record")
@option("tag", char="t", required=True, description="Tag to add")
def add_tag(record, tag):
    """Add a tag to a record."""

    record.add_tag(tag)


@records.command()
@apy_command
@id_identifier_options(class_type="cli_record")
@option("tag", char="t", required=True, description="Tag to remove")
def remove_tag(record, tag):
    """Remove a tag from a record."""

    record.remove_tag(tag)


@records.command()
@apy_command
@id_identifier_options(class_type="cli_record", keep_manager=True)
@id_identifier_options(class_type="record", name="link", helptext="to be linked")
@option("name", char="n", required=True, description="Name of the linking")
def add_record_link(record, link, name):
    """Add a record link to a record."""

    record.link_record(record_to=link, name=name)


@records.command()
@apy_command
@id_identifier_options(class_type="cli_record")
@option(
    "record-link-id",
    char="l",
    required=True,
    description="Record link ID.",
    param_type=Integer,
)
def delete_record_link(record, record_link_id):
    """Delete a record link."""

    record.delete_record_link(record_link_id=record_link_id)


@records.command()
@apy_command
@id_identifier_options(class_type="cli_record")
@option(
    "page",
    char="p",
    description="Page for search results",
    param_type=Integer,
    default=1,
)
@option(
    "direction",
    char="d",
    description="Page for search results",
    param_type=Choice(["to", "from"]),
    default="to",
)
@option(
    "per-page",
    char="n",
    description="Number of results per page",
    param_type=IntRange(1, 100),
    default=10,
)
def show_record_links_to(record, page, per_page, direction):
    """Print record links to another record."""

    record.get_record_links(page=page, per_page=per_page, direction=direction)


@records.command()
@apy_command
@id_identifier_options(class_type="cli_record")
@option("name", char="n", required=True, description="Name of the metadatum")
@option(
    "information",
    char="i",
    required=True,
    description="Specify the information to print",
    param_type=Choice(["value", "unit", "type"]),
)
@option(
    "pipe",
    char="p",
    description="Use this flag if you want to pipe the returned information.",
    is_flag=True,
)
def get_metadatum(record, name, information, pipe):
    """Print a information of a metadatum."""

    record.get_metadatum(name, information, pipe)


@records.command()
@apy_command
@option("tag", char="t", description="Tag(s) for search")
@option("mimetype", char="m", description="MIME types for search")
@option(
    "page",
    char="p",
    description="Page for search results",
    param_type=Integer,
    default=1,
)
@option(
    "per-page",
    char="n",
    description="Number of results per page",
    param_type=IntRange(1, 100),
    default=10,
)
@user_id_options(
    helptext="to show the user's created records.", required=False, keep_manager=True
)
@option(
    "my_user_id",
    char="i",
    description="Show only own created records.",
    is_flag=True,
)
@option(
    "hide-public",
    char="H",
    description="Hide public records.",
    is_flag=True,
)
def get_records(manager, user, my_user_id, **kwargs):
    """Search for records."""

    if kwargs["hide_public"] is False:
        kwargs["hide_public"] = ""

    search = manager.cli_search_resource()

    search.search_resources("record", user=user, my_user_id=my_user_id, **kwargs)


@records.command()
@apy_command
@id_identifier_options(class_type="cli_record")
@file_id_options()
@option("name", char="a", description="The new name of the file.")
@option("mimetype", char="m", description="The new MIME type of the file.")
def edit_file(record, file_id, name, mimetype):
    """Edit the metadata of a file of a record."""

    record.edit_file(file_id, name, mimetype)


@records.command()
@apy_command
@id_identifier_options(class_type="cli_record")
@file_id_options()
def delete_file(record, file_id):
    """Delete a file of a record."""

    record.delete_file(file_id)


@records.command()
@apy_command
@id_identifier_options(class_type="cli_record")
@option(
    "i-am-sure",
    description="Enable this option to delete all files of the record",
    is_flag=True,
)
def delete_files(record, i_am_sure):
    """Delete all files of a record."""

    record.delete_files(i_am_sure)
