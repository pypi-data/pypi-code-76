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
import uuid
from datetime import datetime
from jinja2 import Template

from trainingopz.builders_and_generators.orchestration_artifact_builder.orchestration_artifact_builder import OrchestrationArtifactBuilder
from trainingopz.project_config import ProjectConfig
import traceback


class ArgoArtifactBuilder(OrchestrationArtifactBuilder):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.__manifest_templates = {
            'argo_template': os.path.join(ProjectConfig.package_root(), 'templates/argo_manifest_templates', 'argo_template.yml'),
            'argo_container_template': os.path.join(ProjectConfig.package_root(), 'templates/argo_manifest_templates', 'argo_container_template.yml'),
            'argo_image_template': os.path.join(ProjectConfig.package_root(), 'templates/argo_manifest_templates', 'argo_image_template.yml')
        }

    def _compile_workflow(self, pipe: dict) -> dict:
        try:
            self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:Begin method {__name__}._compile_workflow for {pipe};")
            tasks: list = list()
            containers: list = list()

            argo_stream = open(self.__manifest_templates['argo_template'], 'r').read()
            argo_container_stream = open(self.__manifest_templates['argo_container_template'], 'r').read()
            argo_image_stream = open(self.__manifest_templates['argo_image_template'], 'r').read()

            for task in pipe['workflow']:
                tasks.append(self.__append_task(task, argo_image_stream))
                containers.append(self.__append_container(task, argo_container_stream))

            success = self.__generator_argo(pipe=pipe, tasks=tasks, containers=containers, argo_stream=argo_stream)
            self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:End method {__name__}._compile_workflow;")
            return {'success': success}
        except:
            error_message = traceback.format_exc()
            self._logger.exception(error_message)
            raise RuntimeError(error_message)

    @classmethod
    def __append_container(cls, task: dict, stream: str) -> str:

        task_template = Template(stream, autoescape=True)
        param = ''

        if task.get("parameters"):
            for k, v in task.get("parameters").items():
                param = " --conf " + str(k) + "=" + str(v)

        task_str = task_template.render(
            image_name=task['repo_tagged_docker_image_name'].lower(),
            template_name=task['stage_name'].lower().replace(' ', '-'),
            cmd=task['cmd'] + param)

        return task_str

    def __append_task(self, task: dict, stream: str) -> str:
        self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:Begin method {__name__}.__append_task for {task}, {stream};")
        task_template = Template(stream, autoescape=True)

        dependencies: list = task.get('dependencies')
        if dependencies:
            dependencies = [dep.lower().replace(' ', '-') for dep in dependencies]
        else:
            dependencies = []

        step_name = task['stage_name'].lower().replace(' ', '-')
        task_str = task_template.render(
            dag_name=step_name,
            dependencies=self._generate_dependencies_string(dependencies=dependencies),
            template_name=step_name,
            method_py=task['fit']
        )
        self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:End method {__name__}.__append_task;")
        return task_str

    @classmethod
    def __generator_argo(cls, pipe: dict, tasks: list, containers: list, argo_stream: str) -> bool:

        # TODO Below is very hacky. Will need done right.
        argo_template = Template(argo_stream, autoescape=True)
        argo_str = argo_template.render(
            entrypoint='pipeline',
            generator_name=pipe.get('name').lower().replace(' ', '-')
        ) + '\n' + '\n'.join(tasks) + '\n' + '\n'.join(containers)

        pipeline_name = pipe['name'].lower().replace(" ", "_") + '_argo_' + uuid.uuid4().hex + '.yml'
        # Serialize to manifest YML
        with open(pipeline_name, 'w') as stream:
            stream.write(argo_str)

        pipe['artifact_name'] = pipeline_name

        return True
