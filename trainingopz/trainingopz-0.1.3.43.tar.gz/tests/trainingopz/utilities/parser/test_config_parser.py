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

from trainingopz.utilities.parser.config_parser import ConfigParser


class TestDockerPackager(TestCase):

    def setUp(self) -> None:

        self.__config_parser = ConfigParser()

    def tearDown(self) -> None:
        pass

    @unittest.skip
    def test_parse(self):
        output_conf = {'version': 1,
                       'docker_configuration': {'docker_registry': 'us.gcr.io/ctso-mlops-poc'},
                       'workflow_validation': {
                           'type': 'YAMLValidator',
                           'conf': {
                               'project_path': '../tests/ml_qookeys'
                           }
                       },
                       'pipeline_composition': {
                           'type': 'YAMLPipelineComposer',
                           'conf': {
                               'project_path': '../tests/ml_qookeys'
                           }
                       },
                       'packager': {
                           'type': 'DockerPackager',
                           'conf': {
                               'project_path': '../tests/ml_qookeys'
                           }},
                       'build_deployment_artifact': {
                           'type': 'BuildArgoArtifact',
                           'conf': None
                       },
                       'deploy': {
                           'type': 'ArgoDeployer',
                           'conf': None
                       }}

        output_docker_conf = {'docker_registry': 'us.gcr.io/ctso-mlops-poc'}

        self.__config_parser.parse()

        self.assertDictEqual(self.__config_parser.configuration(), output_conf)
        self.assertDictEqual(self.__config_parser.docker_config(), output_docker_conf)
