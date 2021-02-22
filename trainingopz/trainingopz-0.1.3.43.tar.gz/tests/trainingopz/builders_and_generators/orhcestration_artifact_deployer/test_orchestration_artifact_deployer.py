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

from trainingopz.builders_and_generators.orhcestration_artifact_deployer.orchestration_artifact_deployer import OrchestrationArtifactDeployer
from unittest import TestCase


class TestOrchestrationArtifactDeployer(TestCase):

    def setUp(self) -> None:
        config = {
            'registry': {
                'type': 'GCSRegistry',
                'conf': {
                    'path': ''
                }
            }
        }
        self.__artifact_dep = OrchestrationArtifactDeployer(**config)

    def tearDown(self) -> None:
        pass

    def test_run(self):
        with self.assertRaises(RuntimeError):
            self.__artifact_dep._run('test_pipeline.yml')

    def test_build_part(self):
        val_in = {
            'artifact': [{'name': 'My Test Pipeline', 'artifact_name': 'testname'}],

        }
        with self.assertRaises(RuntimeError):
            self.__artifact_dep.build_part(**val_in)
