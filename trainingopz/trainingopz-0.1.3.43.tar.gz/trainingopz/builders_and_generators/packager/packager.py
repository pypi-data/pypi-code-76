# Copyright © 2020 Hashmap, Inc
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
from trainingopz.builders_and_generators.build_step import BuildStep
from datetime import datetime


class Packager(BuildStep):

    def __init__(self, **kwargs):
        super().__init__()
        self._build_flows: list = list()

    def build_part(self, **kwargs):

        raise NotImplementedError(f'Method not implemented for {type(self).__name__}.')

    def get_results(self):
        self._logger.info(f"INFO>>{datetime.now().__str__()}:Begin method {__name__}.get_results;")
        res = {
            "packager": self._build_flows
        }
        self._logger.info(f"INFO>>{datetime.now().__str__()}:End method {__name__}.get_results;")
        return res
