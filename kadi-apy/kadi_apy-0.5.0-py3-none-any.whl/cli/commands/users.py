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
from xmlhelpy import Integer
from xmlhelpy import IntRange
from xmlhelpy import option

from kadi_apy.cli.decorators import apy_command
from kadi_apy.cli.decorators import user_id_options
from kadi_apy.cli.main import kadi_apy


@kadi_apy.group()
def users():
    """Commands to manage users."""


@users.command()
@apy_command
@user_id_options()
def show_info(user, **kwargs):
    """Show info of a user."""

    user.print_info(**kwargs)


@users.command()
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
    description="To filter the users by their display name or username",
    default=None,
)
def get_users(manager, **kwargs):
    """Search for users."""

    search = manager.cli_search_user()

    search.search_users(**kwargs)
