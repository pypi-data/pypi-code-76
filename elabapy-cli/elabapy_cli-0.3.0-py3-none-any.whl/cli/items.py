# This file is a part of elabftwapy-cli to interact with an elabFTW instance via a CLI
# Copyright (C) 2021 Karlsruhe Institute of Technology
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from xmlhelpy import Integer
from xmlhelpy import option
from xmlhelpy import Path

from elabapy_cli.cli.decorator import apy_command
from elabapy_cli.main import elabapy


@elabapy.group()
def items():
    """Commands to manage items."""


@items.command()
@apy_command
def get_all_items(climanager):
    """Get infos of all items."""

    climanager.get_all_items()


@items.command()
@apy_command
@option(
    "item-id",
    char="i",
    description="ID of the item",
    param_type=Integer,
    required=True,
)
@option(
    "print-json",
    char="j",
    description="Print the hole json",
    param_type=Integer,
    is_flag=True,
)
@option(
    "show-files",
    char="f",
    description="Show the information of attached files.",
    param_type=Integer,
    is_flag=True,
)
def get_item(climanager, item_id, print_json, show_files):
    """Get infos of an item."""

    climanager.get_item(item_id, print_json, show_files)


@items.command()
@apy_command
@option(
    "type",
    char="t",
    description="ID of the item type.",
    param_type=Integer,
    required=True,
)
@option(
    "pipe",
    char="p",
    description="Use this option to print only the id for piping.",
    is_flag=True,
    default=False,
)
def create(climanager, type, pipe):
    """Create an item."""

    climanager.create_item(type, pipe)


@items.command()
@apy_command
def get_items_types(climanager):
    """Get infos of item types."""

    climanager.get_items_types()


@items.command()
@apy_command
@option(
    "item-id",
    char="i",
    description="ID of the item",
    param_type=Integer,
    required=True,
)
@option("title", char="t", default=None, description="New title of the item")
@option("body", char="b", default=None, description="New body of the item")
@option(
    "date",
    char="d",
    default=None,
    description="New date of the item in the form JJJJMMDD",
)
def edit(climanager, item_id, **kwargs):
    """Update title, date or body of an item."""

    climanager.post_item(item_id, **kwargs)


@items.command()
@apy_command
@option(
    "item-id",
    char="i",
    description="ID of the item",
    param_type=Integer,
    required=True,
)
@option(
    "link-id",
    char="l",
    description="ID of the item of the database to be linked",
    required=True,
)
def add_link(climanager, item_id, link_id):
    """Add a link to an item of the database."""

    climanager.add_link_to_item(item_id, link_id)


@items.command()
@apy_command
@option(
    "item-id",
    char="i",
    description="ID of the item",
    param_type=Integer,
    required=True,
)
@option(
    "file_name",
    char="p",
    description="Path to file to upload",
    param_type=Path(exists=True),
    required=True,
)
def upload_to_item(climanager, item_id, file_name):
    """Upload a file to an item."""

    climanager.upload_to_item(item_id, file_name)


@items.command()
@apy_command
@option(
    "item-id",
    char="i",
    description="ID of the item",
    param_type=Integer,
    required=True,
)
@option(
    "tag",
    char="t",
    description="Tag to add to an item",
    required=True,
)
def add_tag(climanager, item_id, tag):
    """Add a tag to an item."""

    climanager.add_tag_to_item(item_id, tag)


@items.command()
@apy_command
def get_bookable(climanager):
    """Show a list of bookable items."""

    climanager.get_bookable()


@items.command()
@apy_command
def get_status(climanager):
    """Show a list of possible statuses of an experiment."""

    climanager.get_status()
