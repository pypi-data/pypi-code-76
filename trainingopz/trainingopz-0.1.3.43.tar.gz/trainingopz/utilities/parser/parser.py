# Modifications © 2020 Hashmap, Inc
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
import os
import traceback

import yaml


class Parser:

    def __init__(self):
        self._path: str = ""
        self._config: dict = {}

    def configuration(self):
        return self._config

    def parse(self):
        try:
            with open(self._path, 'r') as file_stream:
                self._config = yaml.safe_load(file_stream)

            return self

        except:
            error_message = traceback.format_exc()
            raise RuntimeError(error_message)
