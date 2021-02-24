# Copyright 2021 Karlsruhe Institute of Technology
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
from pathlib import Path

from kadi_apy.cli.lib.collections import CLICollection
from kadi_apy.cli.lib.groups import CLIGroup
from kadi_apy.cli.lib.records import CLIRecord
from kadi_apy.cli.lib.templates import CLITemplate
from kadi_apy.lib.exceptions import KadiAPYInputError
from kadi_apy.lib.resources.collections import Collection
from kadi_apy.lib.resources.groups import Group
from kadi_apy.lib.resources.records import Record
from kadi_apy.lib.resources.templates import Template


config_path = Path.home().joinpath(".kadiconfig")

_resource_mapping = {
    "record": Record,
    "collection": Collection,
    "group": Group,
    "template": Template,
    "cli_record": CLIRecord,
    "cli_collection": CLICollection,
    "cli_group": CLIGroup,
    "cli_template": CLITemplate,
}


def resource_mapping(item_type):
    """Map a resource described via string to a class."""

    try:
        return _resource_mapping[item_type]
    except:
        raise KadiAPYInputError(f"Resource type {item_type} does not exists.")
