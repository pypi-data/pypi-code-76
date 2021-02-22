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
from datetime import datetime
import yaml

from trainingopz.builders_and_generators.workflow_validator.workflow_validator import WorkflowValidator


class YAMLValidator(WorkflowValidator):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__full_flow_path = os.path.join(kwargs.get('project_path'), 'workflows', 'flows.yml')

    def _validate(self) -> bool:
        """
        Read in configuration information (for flow reading), read the flow configuration and validate all contents.

        Returns: dictionary with the flows' pipelines

        Raises:
            FileNotFoundError -> flows.yml file was not found
            ValueError -> The contents of the flows.yml file were not correct
        """
        try:
            self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:Begin method {__name__}._validate;")
            self._workflows = dict()

            if not self.__check_if_flow_is_present():
                raise FileNotFoundError('flows.yml not found')

            self.__read_flows()

            errors = self.__get_flow_validation_errors()
            if len(errors) > 0:
                raise ValueError('\n'.join(errors))

            self.__remove_inactive_pipelines()
            self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:End method {__name__}._validate;")
            return True
        except:
            error_message = traceback.format_exc()
            self._logger.exception(error_message)
            raise RuntimeError(error_message)

    def __read_flows(self) -> None:
        """
        Read flows configuration file.

        """
        try:
            self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:Begin method {__name__}.__read_flows;")
            with open(self.__full_flow_path, 'r') as flows_stream:
                self._workflows = yaml.safe_load(flows_stream)
            self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:End method {__name__}.__read_flows;")
        except:
            error_message = traceback.format_exc()
            self._logger.exception(error_message)
            raise RuntimeError(error_message)

    def __check_if_flow_is_present(self) -> bool:
        """
        Check and see if 'flows' file is present.

        Returns: True if file is present, false otherwise.

        """

        return os.path.exists(self.__full_flow_path) and os.path.isfile(self.__full_flow_path)

    def __get_flow_validation_errors(self) -> list:
        """
        Validate the contents of the flows.yml configuration file.

        Returns: False if contents are not: a dictionary, do not contain version or pipelines and
        pipelines is not a list, True otherwise.

        """
        self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:Begin method {__name__}.__get_flow_validation_errors;")
        errors = []
        if not isinstance(self._workflows, dict):
            errors.append(f'Content of {self.__full_flow_path} is not a dictionary.')

        required_keys = {'version', 'pipelines'}
        if not required_keys.intersection(set(self._workflows.keys())):
            errors.append(f'At least one of the required keys - {required_keys} - was not present.')

        if not isinstance(self._workflows['pipelines'], list):
            errors.append(f'In {self.__full_flow_path}, pipelines is not a list.')
        self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:End method {__name__}.__get_flow_validation_errors;")
        return errors

    def __remove_inactive_pipelines(self) -> None:
        """
        Remove pipelines that are not active and have been labeled as such.

        """
        self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:Begin method {__name__}.__remove_inactive_pipelines;")

        self._logger.debug(
            f"DEBUG>>{datetime.now().__str__()}:Begin method {__name__}.__remove_inactive_pipelines;")
        # Capture the pipelines that are active by removing those that are not active.
        pipelines = [flow for flow in self._workflows['pipelines'] if flow['active'] is not False]

        # Update the pipelines with the current ones.
        self._workflows['pipelines'] = pipelines
        self._logger.debug(f"DEBUG>>{datetime.now().__str__()}:End method {__name__}.__remove_inactive_pipelines;")
