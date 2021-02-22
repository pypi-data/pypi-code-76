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

import yaml
from datetime import datetime
from trainingopz.builders_and_generators.pipline_composer.pipeline_composer import PipelineComposer
from trainingopz.exceptions.pipeline_read_error import PipelineReadError


class YAMLPipelineComposer(PipelineComposer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__root_path = kwargs.get('project_path')
        self.__workflows_path = os.path.join(kwargs.get('project_path'), 'workflows')
        self._error_messages = []

    def _build(self, flows: dict) -> list:
        """
        Build and return a dict containing the information about all pipelines that will need to be built. The contents
        of the specification will be validated.

        Args:
            flows: dictionary of all active flows

        Returns: flushed out pipeline flows as will be needed for building the containers

        """
        try:
            self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:Begin method {__name__}.build for {flows};")
            # Future Version will need to handle different schema versions via factory
            res = [self.__build_flow(pipeline) for pipeline in flows['pipelines']]
            self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:End method {__name__}.build;")
            return res
        except:
            error_message = traceback.format_exc()
            self._logger.exception(error_message)
            raise RuntimeError(error_message)

    def __build_flow(self, pipeline: dict) -> None:
        self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:Begin method {__name__}.__build_flow for {pipeline};")
        # Read the pipeline yaml file
        pipeline_config_path = os.path.join(self.__workflows_path, 'pipelines', pipeline['name'] + '.yml')

        with open(pipeline_config_path, 'r') as fh:
            pipeline = yaml.safe_load(fh)

        self.__validate_pipeline(pipeline)

        if len(self._error_messages) > 0:
            self.__log_build_results()
            raise PipelineReadError("\n".join(self._error_messages))

        # get the workflow
        self._pipelines.append(pipeline)
        self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:Begin method {__name__}.__build_flow;")

    def __validate_pipeline(self, pipeline: dict) -> None:
        self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:Begin method {__name__}.__validate_pipeline for {pipeline};")
        keys = [key.lower() for key in pipeline.keys()]
        required_keys = {'project_root', 'workflow', 'version', 'stages'}
        # Stages has root and workflow
        if not required_keys.intersection(keys):
            self._generate_validation_message(f'At least one of {required_keys} is missing from configuration.')

        workflow: dict = pipeline.get('workflow')
        # Workflow is list
        if not isinstance(workflow, list):
            self._generate_validation_message(f'"workflow" must be a list.')

        # Workflow components are dicts
        if any([1 for node in workflow if not isinstance(node, dict)]):
            self._generate_validation_message(f'All entries in the workflow must be a dictionary.')

        # Workflow component path and files exist and is a python file
        _ = [self.__validate_nodes(node=node) for node in workflow]

        # Get list of all dependencies
        dependency_lists = [node.get('dependencies') for node in workflow if 'dependencies' in node.keys()]
        dependencies = []
        _ = [dependencies.extend(dependency) for dependency in dependency_lists]
        dependencies = list(set(dependencies))

        _ = [self.__validate_dependencies(all_dependencies=dependencies, node=node) for node in workflow]
        self._logger.debug(
            f"DEBUG>>{datetime.now().__str__()}:End method {__name__}.__validate_pipeline;")

    def __log_build_results(self) -> None:
        self._logger.error("\n".join(self._error_messages))

    def __validate_nodes(self, node: dict) -> None:

        keys = [key.lower() for key in node.keys()]
        if 'stage_name' not in keys:
            self._generate_validation_message("in workflow not 'stage_name' found.")

        if 'fit' not in keys:
            self._generate_validation_message("in workflow not 'fit' found.")

        if 'type' not in keys:
            self._generate_validation_message("in workflow not 'type' found.")

        entrypoint = os.path.join(self.__root_path, node.get('fit'))
        if not os.path.exists(entrypoint):
            self._generate_validation_message(f'fit {entrypoint} does not exist.')

        if not os.path.isfile(entrypoint):
            self._generate_validation_message(f'fit {entrypoint} is not a file')

    def _generate_validation_message(self, message: str) -> None:
        return self._error_messages.append(f'In {__name__}: {message}')

    def __validate_dependencies(self, all_dependencies: list, node: dict) -> None:

        keys = [key.lower() for key in node.keys()]

        if 'dependencies' not in keys:
            return

        dependencies = node.get('dependencies')
        if not isinstance(dependencies, list):
            self._generate_validation_message(f'dependencies is not a list.')

        if any([1 for dependency in dependencies if dependency not in all_dependencies]):
            self._generate_validation_message(f'dependency was not tracked in ')
