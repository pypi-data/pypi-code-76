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
# import requests
# import subprocess
from datetime import datetime
from trainingopz.exceptions.airflow_deployer_error import AirflowDeployerError
from trainingopz.builders_and_generators.orhcestration_artifact_deployer.orchestration_artifact_deployer import OrchestrationArtifactDeployer


class AirflowDeployer(OrchestrationArtifactDeployer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._path = kwargs.get('path')

    def _run(self, artifact: str):

        try:
            self._logger.info(f"INFO>>{datetime.now().__str__()}:Begin method {__name__}._run for {artifact};")
            # rc = self._deploy(artifact)
            self._logger.info(f"INFO>>{datetime.now().__str__()}:End method {__name__}._run;")
        except:
            error_message = traceback.format_exc()
            self._logger.exception(error_message)
            raise AirflowDeployerError(error_message)

        return True

    # def _deploy(self, artifact):
    #
    # # head = { #         'Cache-Control': 'no-cache', #         'Content-Type': 'application/json' # # } # url =
    # f'http://localhost:8080/api/experimental/dags/{artifact}/dag_runs' # data = { #     "replace_microseconds":
    # "false" # } # ret_code = requests.post(url=url, headers=head, data=data) self.result = subprocess.run([
    # 'airflow', 'dags', 'trigger', "my_test_pipeline"], check=True, stderr=subprocess.STDOUT) print(self.result)
    # return self.result
