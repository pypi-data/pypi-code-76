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
from kadi_apy.cli.main import kadi_apy


@kadi_apy.group()
def templates():
    """Commands to manage templates."""


@templates.command()
@apy_command
@option(
    "identifier",
    char="i",
    required=True,
    description="Identifier of the template",
    default=None,
)
@option("title", char="t", description="Title of the template")
@option(
    "type",
    char="y",
    description="Type of the template",
    param_type=Choice(["extras", "record"]),
    default="record",
)
@option(
    "pipe",
    char="p",
    description="Use this flag if you want to pipe the returned template id.",
    is_flag=True,
)
@option(
    "data",
    char="d",
    description="Data for the template",
    default=None,
)
def create(manager, **kwargs):
    """Create a template."""

    if kwargs["data"] is None:
        if kwargs["type"] == "record":
            kwargs["data"] = {}
        else:
            kwargs["data"] = []

    manager.cli_template(create=True, **kwargs)


@templates.command()
@apy_command
@id_identifier_options(class_type="template", helptext="to delete")
@option(
    "i-am-sure", description="Enable this option to delete the template", is_flag=True
)
def delete(template, i_am_sure):
    """Delete a template."""

    template.delete(i_am_sure)


@templates.command()
@apy_command
@option("page", char="p", description="Page for search results", param_type=Integer)
@option(
    "per-page",
    char="n",
    description="Number of results per page",
    param_type=IntRange(1, 100),
    default=10,
)
def get_templates(manager, **kwargs):
    """Search for templates."""

    search = manager.cli_search_resource()

    search.search_resources("template", **kwargs)
