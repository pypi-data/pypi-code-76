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
from typing import List
import traceback
from jinja2 import Template
from datetime import datetime
from trainingopz.builders_and_generators.orchestration_artifact_builder.orchestration_artifact_builder import \
    OrchestrationArtifactBuilder

from trainingopz.project_config import ProjectConfig


class AirflowArtifactBuilder(OrchestrationArtifactBuilder):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.__manifest_templates = {
            'airflow_k8_template': os.path.join(ProjectConfig.package_root(), 'templates/airflow_templates',
                                                'airflow_k8_operator_template'),
            'airflow_dag_template': os.path.join(ProjectConfig.package_root(), 'templates/airflow_templates',
                                                 'airflow_dag_template')
        }

        self.__namespace = kwargs.get('namespace')

    def _compile_workflow(self, pipe: dict) -> dict:
        try:

            self._logger.debug(
                f"DEBUG>>{datetime.now().__str__()}:Begin method {__name__}._compile_workflow for {pipe};")
            tasks: list = list()
            dep = dict()
            for task in pipe['workflow']:
                tasks.append(self.__append_task(task))
                if not dep.get(task["stage_name"]):
                    dep[task["stage_name"]] = task.get('dependencies')
                else:
                    dep[task["stage_name"]].extend(task.get('dependencies'))

            success = self.__generator_airflow(pipe=pipe, tasks=tasks, dep=dep)
            self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:End method {__name__}._compile_workflow;")
            return {
                'success': success,
            }
        except:
            error_message = traceback.format_exc()
            self._logger.exception(error_message)
            raise RuntimeError(error_message)

    def __append_task(self, task):
        self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:Begin method {__name__}.__append_task for {task};")
        with open(self.__manifest_templates['airflow_k8_template'], 'r') as f:
            k8_temp = f.read()
        param = ''

        if task.get("parameters"):
            for k, v in task.get("parameters").items():
                param = " --conf " + str(k) + "=" + str(v)

        script = task.get("fit").replace("\\", "\\\\")
        # TOdo below technique might have to change with generic one
        cmd = task.get('cmd').lower() + ' ' + param + script

        k8_template = Template(k8_temp, autoescape=True)
        task_str = k8_template.render(
            stage=task.get("stage_name").lower().replace(" ", "_"),
            img=task.get("repo_tagged_docker_image_name"),
            cmds=cmd.split(" "),
            namespace=self.__namespace
        )
        self._logger.debug(f"DEBUG>>{datetime.now().__str__()}: End method {__name__}.__append_task;")
        return task_str

    def __build_dep(self, dep):
        self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:Begin method {__name__}.__build_dep for {dep};")
        dep_str = ""

        for task in dep.keys():
            if dep[task]:
                t = [v.lower().replace(" ", "_") for v in dep[task]]
                dep_str += f"""{str(t).replace("'", "")} >> {task.lower().replace(" ", "_")}\n"""
            else:
                dep_str += f"""{task.lower().replace(" ", "_")}\n"""
        self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:End method {__name__}.__build_dep;")
        return dep_str

    def __generator_airflow(self, pipe: dict, tasks: list, dep: dict):
        self._logger.debug(
            f"DEBUG>>{datetime.now().__str__()}:Begin method {__name__}.__generator_airflow for {pipe}, {tasks}, {dep};")
        pipeline_name = pipe['name'].lower().replace(" ", "_")

        with open(self.__manifest_templates['airflow_dag_template'], 'r') as f:
            dag_temp = f.read()
        pipeline_name = pipeline_name + '_airflow_' + uuid.uuid4().hex
        dag_template = Template(dag_temp, autoescape=True)
        airflow_str = dag_template.render(desc="Automated Training Pipeline", name=pipeline_name) + "\n" + "\n".join(
            tasks) + "\n" + self.__build_dep(dep)
        pipeline_name = pipeline_name + '.py'
        # TODO This shouldn't be hard-coded and should be by 'run'
        with open(pipeline_name, 'w') as stream:
            stream.write(airflow_str)

        pipe['artifact_name'] = pipeline_name
        self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:End method {__name__}.__generator_airflow;")
        return True
