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

from kadi_apy.cli.decorators import apy_command
from kadi_apy.cli.decorators import id_identifier_options
from kadi_apy.cli.decorators import user_id_options
from kadi_apy.cli.main import kadi_apy


@kadi_apy.group()
def collections():
    """Commands to manage collections."""


@collections.command()
@apy_command
@option("title", char="t", description="Title of the collection")
@option(
    "identifier",
    char="i",
    required=True,
    description="Identifier of the collection",
    default=None,
)
@option(
    "visibility",
    char="v",
    description="Visibility of the collection",
    default="private",
    param_type=Choice(["private", "public"]),
)
@option(
    "pipe",
    char="p",
    description="Use this flag if you want to pipe the returned collection id.",
    is_flag=True,
)
def create(manager, **kwargs):
    """Create a collection."""

    manager.cli_collection(**kwargs, create=True)


@collections.command()
@apy_command
@id_identifier_options(class_type="cli_collection", helptext="to edit")
@option(
    "visibility",
    char="v",
    description="Visibility of the collection to set",
    default=None,
    param_type=Choice(["private", "public"]),
)
@option("title", char="t", default=None, description="Title of the collection to set")
@option(
    "description",
    char="d",
    default=None,
    description="Description of the collection to set",
)
def edit(collection, visibility, title, description):
    """Edit visibility, title or description of a collection."""

    collection.set_attribute(
        visibility=visibility, title=title, description=description
    )


@collections.command()
@apy_command
@id_identifier_options(class_type="cli_collection")
@option(
    "description",
    char="d",
    description="Show the description of the collection",
    is_flag=True,
    default=False,
)
@option(
    "visibility",
    char="v",
    description="Show the visibility of the collection",
    is_flag=True,
    default=False,
)
@option(
    "records",
    char="r",
    description="Show linked records of the collection",
    is_flag=True,
    default=False,
)
@option(
    "page", char="p", description="Page for records list", param_type=Integer, default=1
)
@option(
    "per-page",
    char="n",
    description="Number of results per page",
    param_type=IntRange(1, 100),
    default=10,
)
def show_info(collection, **kwargs):
    """Show info of a collection."""

    collection.print_info(**kwargs)


@collections.command()
@apy_command
@id_identifier_options(
    class_type="cli_collection", helptext="to add the user", keep_manager=True
)
@user_id_options()
@option(
    "permission-new",
    char="p",
    description="Permission of new user",
    default="member",
    param_type=Choice(["member", "editor", "admin"]),
)
def add_user(collection, user, permission_new):
    """Add a user to a collection."""

    collection.add_user(user=user, permission_new=permission_new)


@collections.command()
@apy_command
@id_identifier_options(
    class_type="cli_collection", helptext="to remove the user", keep_manager=True
)
@user_id_options()
def remove_user(collection, user):
    """Remove a user from a collection."""

    collection.remove_user(user=user)


@collections.command()
@apy_command
@id_identifier_options(
    class_type="cli_collection",
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
def add_group_role(collection, group, permission_new):
    """Add a group role to a collection."""

    collection.add_group_role(group, permission_new)


@collections.command()
@apy_command
@id_identifier_options(
    class_type="cli_collection", helptext="to remove the group", keep_manager=True
)
@id_identifier_options(class_type="group")
def remove_group_role(collection, group):
    """Remove a group role from a collection."""

    collection.remove_group_role(group)


@collections.command()
@apy_command
@id_identifier_options(class_type="cli_collection", helptext="to delete")
@option(
    "i-am-sure", description="Enable this option to delete the collection", is_flag=True
)
def delete(collection, i_am_sure):
    """Delete a collection."""

    collection.delete(i_am_sure)


@collections.command()
@apy_command
@id_identifier_options(
    class_type="cli_collection", helptext="to link to the record", keep_manager=True
)
@id_identifier_options(class_type="record", helptext="to link to the collection")
def add_record_link(collection, record):
    """Link record to a collection."""

    collection.add_record_link(record_to=record)


@collections.command()
@apy_command
@id_identifier_options(
    class_type="cli_collection", helptext="to remove the record", keep_manager=True
)
@id_identifier_options(class_type="record", helptext="to remove from the collection")
def remove_record_link(collection, record):
    """Remove a record link from a collection."""

    collection.remove_record_link(record)


@collections.command()
@apy_command
@id_identifier_options(class_type="cli_collection", helptext="to add a tag")
@option("tag", char="t", required=True, description="Tag to add")
def add_tag(collection, tag):
    """Add a tag to a collection."""

    collection.add_tag(tag)


@collections.command()
@apy_command
@id_identifier_options(class_type="cli_collection", helptext="to remove a tag")
@option("tag", char="t", required=True, description="Tag to remove")
def remove_tag(collection, tag):
    """Remove a tag from a collection."""

    collection.remove_tag(tag)


@collections.command()
@apy_command
@option("tag", char="t", description="Tag(s) for search")
@option("page", char="p", description="Page for search results", param_type=Integer)
@option(
    "per-page",
    char="n",
    description="Number of results per page",
    param_type=IntRange(1, 100),
    default=10,
)
@user_id_options(
    helptext="to show the user's created collections.",
    required=False,
    keep_manager=True,
)
@option(
    "my_user_id",
    char="i",
    description="Show only own created collections.",
    is_flag=True,
)
@option(
    "hide-public",
    char="H",
    description="Hide public records.",
    is_flag=True,
)
def get_collections(manager, user, my_user_id, **kwargs):
    """Search for collections."""

    if kwargs["hide_public"] is False:
        kwargs["hide_public"] = ""

    search = manager.cli_search_resource()

    search.search_resources("collection", user=user, my_user_id=my_user_id, **kwargs)
