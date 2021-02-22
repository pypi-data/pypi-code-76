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
import os
import traceback
import uuid

from jinja2 import Template
from datetime import datetime
from trainingopz.builders_and_generators.orchestration_artifact_builder.orchestration_artifact_builder import \
    OrchestrationArtifactBuilder
from trainingopz.project_config import ProjectConfig


class FileArtifactBuilder(OrchestrationArtifactBuilder):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.__manifest_templates = {
            'file_template': os.path.join(ProjectConfig.package_root(), 'templates/file_manifest_templates',
                                          'file_template.yml'),
            'file_manifest_template': os.path.join(ProjectConfig.package_root(), 'templates/file_manifest_templates',
                                                   'file_manifest_template.yml'),
        }
        self._target_dir = '.'
        if kwargs.get("target_dir"):
            self._target_dir = kwargs.get("target_dir")

    def _compile_workflow(self, pipe: dict) -> dict:
        try:
            self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:Begin method {__name__}.\
                                                    _compile_workflow for {pipe};")
            tasks: list = []

            file_template = open(self.__manifest_templates['file_template'], 'r').read()

            for sc in pipe['workflow']:
                tasks.append(self.__append_task(sc, file_template))

            success = self.__generator_manifest(pipe=pipe, tasks=tasks)
            self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:End method {__name__}.\
                                                    _compile_workflow;")
            return {'success': success}
        except:
            error_message = traceback.format_exc()
            self._logger.exception(error_message)
            raise RuntimeError(error_message)

    def __append_task(self, sc, file_template):
        self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:Begin method {__name__}.\
                                                __append_task for {sc}, {file_template};")
        file_template = Template(file_template, autoescape=True)
        cmd2exe = "cp " + sc + " " + self._target_dir

        file_str = file_template.render(script=cmd2exe)+"\n"
        self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:End method {__name__}.\
                                                        __append_task;")
        return file_str

    @classmethod
    def __generator_manifest(cls, pipe: dict, tasks: list) -> bool:

        files_str = "".join(tasks)
        manifest_name = pipe['name'].lower().replace(" ", "_") + '_file_' + uuid.uuid4().hex + '.sh'

        with open(manifest_name, 'w') as file_fp:
            file_fp.write(files_str)

        pipe['artifact_name'] = manifest_name
        return True

