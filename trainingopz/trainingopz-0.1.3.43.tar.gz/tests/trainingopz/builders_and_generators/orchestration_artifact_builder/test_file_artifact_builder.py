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
from trainingopz.builders_and_generators.orchestration_artifact_builder.file_artifact_builder import FileArtifactBuilder
from unittest import TestCase
import os


class TestFileArtifactBuilder(TestCase):

    def setUp(self) -> None:
        configuration = dict(
            project_path=os.path.abspath('../../test_output_dir'),
            target_dir=os.path.abspath('../../test_output_dir')
        )
        self.__artifact_builder = FileArtifactBuilder(**configuration)

    def tearDown(self) -> None:
        pass

    def test_compile_workflow(self):
        val_in = {
                    "name": 'test pipe',
                    'workflow': []
        }
        self.assertTrue(self.__artifact_builder._compile_workflow(val_in))
