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

from unittest import TestCase
import unittest
from trainingopz.utilities.parser.cmd_config_parser import CmdConfigParser


class TestCmdConfigParser(TestCase):

    def setUp(self) -> None:
        self.__cmd_parser = CmdConfigParser()

    def tearDown(self) -> None:
        pass

    @unittest.skip
    def test_parse(self):

        output_worflow = {
            'version': 1,
            'pyspark_with_gpu': {
                'cmd': 'spark-submit',
                'parameters': {
                    'mem': 20, 'cores': 4, 'master': 'yarn'
                }},
            'pyspark_highmem': {'cmd': 'spark-submit',
                                'parameters': {'mem': 20, 'master': 'yarn'}},
            'pyspark_with_mem2': {
                                  'cmd': 'spark-submit',
                                  'parameters': {'mem': 40, 'cores': 4, 'master': 'yarn'}},
            'pyspark1.6': {
                         'cmd': 'spark-submit',
                         'parameters': {'mem': 20, 'cores': 4, 'master': 'yarn'}},
            'python_with_ml': {'cmd': 'python3'},
            'for_R': {'cmd': 'r'}}

        self.__cmd_parser.parse()
        self.assertDictEqual(self.__cmd_parser.configuration(), output_worflow)
