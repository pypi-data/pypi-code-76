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
from kadi_apy.cli.commons import item_add_user
from kadi_apy.cli.commons import item_delete
from kadi_apy.cli.commons import item_print_info
from kadi_apy.cli.commons import item_remove_user
from kadi_apy.cli.commons import item_set_attribute
from kadi_apy.cli.commons import print_item_created
from kadi_apy.lib.resources.groups import Group


class CLIGroup(Group):
    """Group class to be used in a cli."""

    def __init__(self, pipe=False, title=None, create=False, **kwargs):
        super().__init__(title=title, create=create, **kwargs)

        print_item_created(self, title=title, pipe=pipe, create=create)

    def set_attribute(self, **kwargs):
        # pylint: disable=arguments-differ
        return item_set_attribute(self, **kwargs)

    def print_info(self, **kwargs):
        """Print group infos."""

        return item_print_info(self, **kwargs)

    def add_user(self, user, permission_new):
        # pylint: disable=arguments-differ
        return item_add_user(self, user=user, permission_new=permission_new)

    def remove_user(self, user):
        # pylint: disable=arguments-differ
        return item_remove_user(self, user=user)

    def delete(self, i_am_sure):
        # pylint: disable=arguments-differ
        return item_delete(self, i_am_sure=i_am_sure)
