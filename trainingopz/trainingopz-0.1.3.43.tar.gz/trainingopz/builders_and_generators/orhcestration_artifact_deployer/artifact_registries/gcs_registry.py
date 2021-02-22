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
import subprocess
import traceback
from datetime import datetime
from trainingopz.builders_and_generators.orhcestration_artifact_deployer.artifact_registries.artifact_registry import ArtifactRegistry


class GCSRegistry(ArtifactRegistry):

    def __init__(self, **kwargs):
        super().__init__()
        self.__path = kwargs.get('path')

    def register(self, artifact):
        try:
            self._logger.info(f"INFO>>{datetime.now().__str__()}:Begin method {__name__}.register for {artifact};")
            subprocess.run(['gsutil', 'cp', artifact, self.__path], check=True, stderr=subprocess.STDOUT)
            self._logger.info(f"INFO>>{datetime.now().__str__()}:Begin method {__name__}.register")
        except:
            error_message = traceback.format_exc()
            self._logger.exception(error_message)
            raise RuntimeError(error_message)