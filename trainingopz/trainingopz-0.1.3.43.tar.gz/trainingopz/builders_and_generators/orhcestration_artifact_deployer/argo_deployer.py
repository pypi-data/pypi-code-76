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
import subprocess
import traceback
from datetime import datetime
from trainingopz.builders_and_generators.orhcestration_artifact_deployer.orchestration_artifact_deployer import OrchestrationArtifactDeployer
from trainingopz.exceptions.argo_deployer_error import ArgoDeployerError


class ArgoDeployer(OrchestrationArtifactDeployer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__namespace = kwargs.get('namespace')
        if not self.__namespace:
            self.__namespace = 'argo'
        self.result = None

    def _run(self, artifact: str):

        try:
            print("running argo deployer... ")
            self._logger.info(f"INFO>>{datetime.now().__str__()}:Begin method {__name__}._run for {artifact};")
            self.result = subprocess.run(['argo', 'submit', '-n', self.__namespace, artifact], check=True, stderr=subprocess.STDOUT)

            if self.result.stderr:
                print('Standard Error: ', self.result.stderr)
            self._logger.info(f"INFO>>{datetime.now().__str__()}:End method {__name__}._run;")
            return True

        except:
            error_message = traceback.format_exc()
            self._logger.exception(error_message)
            raise ArgoDeployerError(error_message)
