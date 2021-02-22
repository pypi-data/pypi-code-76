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
import traceback

from providah.factories.package_factory import PackageFactory as pf
import os
from datetime import datetime
from trainingopz.builders_and_generators.build_step import BuildStep
from trainingopz.builders_and_generators.orhcestration_artifact_deployer.artifact_registries.artifact_registry import ArtifactRegistry
from trainingopz.exceptions.deploy_script_generation_error import DeployScriptGenerationError


class OrchestrationArtifactDeployer(BuildStep):

    def __init__(self, **kwargs):
        super().__init__()
        self._workflow = list()
        reg_conf = kwargs.get('registry')
        self._registry: ArtifactRegistry = pf.create(key=reg_conf.get('type'), configuration=reg_conf.get('conf'))

    def build_part(self, **kwargs):
        try:
            self._logger.info(f"INFO>>{datetime.now().__str__()}:Begin method {__name__}.build_part for {kwargs};")
            _res = True
            for pipe in kwargs.get("artifact"):
                self._registry.register(artifact=pipe['artifact_name'])
                _res = _res and self._run(artifact=pipe['artifact_name'])

                os.remove(pipe['artifact_name'])

            if not _res:
                raise DeployScriptGenerationError()
            self._logger.info(f"INFO>>{datetime.now().__str__()}:End method {__name__}.build_part;")
            return True

        except:
            error_message = traceback.format_exc()
            self._logger.exception(error_message)
            raise RuntimeError(error_message)

    def _run(self, artifact: str):
        raise NotImplementedError(f'Method not implemented for {type(self).__name__}.')

    def get_results(self):
        self._logger.info(f"INFO>>{datetime.now().__str__()}:Begin method {__name__}.get_results;")
        result = dict()
        if len(self._workflow) > 0:
            result = {
                "deployer": self._workflow
            }
        self._logger.info(f"INFO>>{datetime.now().__str__()}:End method {__name__}.get_results;")
        return result
