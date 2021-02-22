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
from typing import NamedTuple

from trainingopz.builders_and_generators.orchestration_artifact_builder.orchestration_artifact_builder import OrchestrationArtifactBuilder
from trainingopz.builders_and_generators.orhcestration_artifact_deployer.orchestration_artifact_deployer import OrchestrationArtifactDeployer
from trainingopz.builders_and_generators.packager.packager import Packager
from trainingopz.builders_and_generators.pipline_composer.pipeline_composer import PipelineComposer
from trainingopz.builders_and_generators.workflow_validator.workflow_validator import WorkflowValidator


class BuildPipeline(NamedTuple):
    workflow_validator: WorkflowValidator
    pipeline_composer: PipelineComposer
    packager: Packager
    deployment_artifact_builder: OrchestrationArtifactBuilder
    deployer: OrchestrationArtifactDeployer
