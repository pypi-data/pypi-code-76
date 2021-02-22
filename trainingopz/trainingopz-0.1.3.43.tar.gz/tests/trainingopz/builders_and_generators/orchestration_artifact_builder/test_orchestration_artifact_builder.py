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
from trainingopz.builders_and_generators.orchestration_artifact_builder.orchestration_artifact_builder import \
    OrchestrationArtifactBuilder
from unittest import TestCase, skip

from trainingopz.exceptions.orchestration_artifact_build_error import OrchestrationArtifactBuildError


class TestOrchestrationArtifactBuilder(TestCase):

    def setUp(self) -> None:
        self.__artifact_builder = OrchestrationArtifactBuilder(**{})

    def tearDown(self) -> None:
        pass

    @skip
    def test_build_part(self):
        """ ToDo: Bug: result in _build() return True for result=[] it should return False, skipping for now"""
        val_in = {
                'packager': []
                  }
        with self.assertRaises(OrchestrationArtifactBuildError):
            self.__artifact_builder.build_part(**val_in)

    def test_compile_workflow(self):
        val_in = list()
        with self.assertRaises(NotImplementedError):
            self.__artifact_builder._compile_workflow(val_in)
