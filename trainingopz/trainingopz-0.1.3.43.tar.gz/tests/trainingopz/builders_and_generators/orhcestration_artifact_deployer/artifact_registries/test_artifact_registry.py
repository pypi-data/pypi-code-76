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
from trainingopz.builders_and_generators.orhcestration_artifact_deployer.artifact_registries.artifact_registry import ArtifactRegistry


class TestArtifactRegistry(TestCase):

    def setUp(self) -> None:

        self.__artifact_reg = ArtifactRegistry()

    def tearDown(self) -> None:
        pass

    def test_register(self):
        with self.assertRaises(NotImplementedError):
            self.__artifact_reg.register("artifact")
