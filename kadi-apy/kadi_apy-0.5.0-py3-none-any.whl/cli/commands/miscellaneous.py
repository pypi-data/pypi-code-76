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
from kadi_apy.cli.main import kadi_apy
from kadi_apy.lib.resources.collections import Collection
from kadi_apy.lib.resources.groups import Group
from kadi_apy.lib.resources.records import Record

_resource_mapping = {"record": Record, "collection": Collection, "group": Group}


@kadi_apy.group()
def miscellaneous():
    """Commands to manage miscellaneous."""


@miscellaneous.command()
@apy_command
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
@option(
    "filter",
    char="f",
    description="Filter by title or identifier.",
    default="",
)
def get_deleted_resources(manager, **kwargs):
    """Show a list of deleted resources in the trash."""

    manager.cli_misc.get_deleted_resources(**kwargs)


@miscellaneous.command()
@apy_command
@option(
    "item-type",
    char="t",
    description="Type of the resource to restore",
    param_type=Choice(list(_resource_mapping.keys())),
    required=True,
)
@option(
    "item-id",
    char="i",
    description="ID of the resource to restore.",
    default="",
)
def restore_resource(manager, item_type, item_id):
    """Restore a resource from the trash."""

    item = _resource_mapping[item_type]

    manager.cli_misc.restore(item=item, item_id=item_id)


@miscellaneous.command()
@apy_command
@option(
    "item-type",
    char="t",
    description="Type of the resource to restore",
    param_type=Choice(list(_resource_mapping.keys())),
    required=True,
)
@option(
    "item-id",
    char="i",
    description="ID of the resource to restore.",
    default="",
)
def purge_resource(manager, item_type, item_id):
    """Purge a resource from the trash."""

    item = _resource_mapping[item_type]

    manager.cli_misc.purge(item=item, item_id=item_id)


@miscellaneous.command()
@apy_command
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
@option(
    "filter",
    char="f",
    description="Filter.",
    default="",
)
def get_licenses(manager, **kwargs):
    """Show a list available licenses."""

    manager.cli_misc.get_licenses(**kwargs)
