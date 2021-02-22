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
from unittest import TestCase

from trainingopz.exceptions.container_build_error import ContainerBuildError
from trainingopz.exceptions.deploy_script_generation_error import DeployScriptGenerationError
from trainingopz.exceptions.docker_file_create_error import DockerFileCreateError
from trainingopz.exceptions.flow_build_error import FlowBuildError
from trainingopz.exceptions.flow_validation_error import FlowValidationError
from trainingopz.exceptions.ml_error import MLError
from trainingopz.exceptions.orchestration_artifact_build_error import OrchestrationArtifactBuildError
from trainingopz.exceptions.pipeline_read_error import PipelineReadError
from trainingopz.exceptions.packager_error import PackagerError
from trainingopz.exceptions.file_deployer_error import FileDeployerError
from trainingopz.exceptions.argo_deployer_error import ArgoDeployerError
from trainingopz.exceptions.airflow_deployer_error import AirflowDeployerError



class TestCustomException(TestCase):

    def test_custom_exception(self):

        with self.assertRaises(ContainerBuildError):
            raise ContainerBuildError

        with self.assertRaises(DeployScriptGenerationError):
            raise DeployScriptGenerationError

        with self.assertRaises(DockerFileCreateError):
            raise DockerFileCreateError

        with self.assertRaises(FlowBuildError):
            raise FlowBuildError

        with self.assertRaises(FlowValidationError):
            raise FlowValidationError

        with self.assertRaises(OrchestrationArtifactBuildError):
            raise OrchestrationArtifactBuildError

        with self.assertRaises(MLError):
            raise MLError

        with self.assertRaises(PipelineReadError):
            raise PipelineReadError

        with self.assertRaises(PackagerError):
            raise PackagerError

        with self.assertRaises(FileDeployerError):
            raise FileDeployerError

        with self.assertRaises(AirflowDeployerError):
            raise AirflowDeployerError

        with self.assertRaises(ArgoDeployerError):
            raise ArgoDeployerError
