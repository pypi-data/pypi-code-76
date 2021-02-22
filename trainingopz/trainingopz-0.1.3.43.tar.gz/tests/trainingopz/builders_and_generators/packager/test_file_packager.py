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
import os
from unittest import TestCase
import unittest

from trainingopz.builders_and_generators.packager.file_packager import FilePackager
from trainingopz.builders_and_generators.packager.packager import Packager
from trainingopz.exceptions.packager_error import PackagerError


class TestFilePackager(TestCase):

    def setUp(self) -> None:
        configuration = dict(
            project_path=os.path.abspath('../../test_output_dir')
        )
        self.__packager = FilePackager(**configuration)

    def tearDown(self) -> None:
        pass

    def test_ctor(self):
        configuration = dict(
            project_path=os.path.abspath('../../test_output_dir')
        )
        packager = FilePackager(**configuration)

        self.assertIsInstance(packager, FilePackager)
        self.assertIsInstance(packager, Packager)
        self.assertDictEqual(self.__packager.get_results(), dict(packager=[]))

    @unittest.skip
    def test_get_results(self):
        self.assertDictEqual(self.__packager.get_results(), dict(Packager=[]))

    @unittest.skip
    def test_build_part_incorrect_input(self):
        with self.assertRaises(PackagerError):
            self.__packager.build_part(**{})

    @unittest.skip
    def test_build_part_single_stage(self):
        configuration = dict(
            flows=[{
                'project_root': 'stages',
                'workflow': [{
                    'stage_name': 'Process Data',
                    'entry_point': 'hello.py',
                    'type': 'python_with_ml'
                }]
            }]
        )

        self.__packager.build_part(**configuration)

    @unittest.skip
    def test_build_part_multi_stage_1(self):
        configuration = dict(
            flows=[{
                'project_root': '.',
                'workflow': [
                    {
                        'stage_name': 'Process Data 1',
                        'entry_point': 'src/data_processing/process_1.py',
                        'type': 'python'
                    },
                    {
                        'stage_name': 'Process Data 2',
                        'entry_point': 'src/data_processing/process_2.py',
                        'type': 'python'
                    }
                ]
            }]
        )

        self.__packager.build_part(**configuration)
        pass

    @unittest.skip
    def build_part_multi_stage_2(self):
        configuration = dict(
            flows=[{
                'project_root': 'stages',
                'workflow': [
                    {
                        'stage_name': 'Process Data 1',
                        'entry_point': 'src/data_processing/process_1.py',
                        'type': 'python'
                    },
                    {
                        'stage_name': 'Process Data 2',
                        'entry_point': 'src/data_processing/process_2.py',
                        'type': 'python',
                        'dependencies': ['Process Data 1']
                    }
                ]
            }]
        )

        self.__packager.build_part(**configuration)
