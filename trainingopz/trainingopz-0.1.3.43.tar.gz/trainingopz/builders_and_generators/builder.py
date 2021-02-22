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
import logging
import traceback
from datetime import datetime
import yaml
from providah.factories.package_factory import PackageFactory as pf
from trainingopz.logger.ml_log import MLLog
from trainingopz.builders_and_generators.build_pipeline import BuildPipeline
from trainingopz.project_config import ProjectConfig


class Builder:

    def __init__(self, **kwargs):
        self._logger = MLLog("Builder", logging.DEBUG, True).logger
        self.__path = kwargs.get("project_path")
        self.__build_pipeline = BuildPipeline

    @property
    def pipeline(self):
        return self.__build_pipeline

    def build(self):
        self._logger.info(f"INFO>>{datetime.now().__str__()}:Begin method {__name__}.build;")
        try:
            # Configuration is lazy
            with open(ProjectConfig.config_path(), 'r') as stream:
                configuration = yaml.safe_load(stream)

            if self.__path:
                configuration['workflow_validation']['conf']['project_path'] = self.__path
                configuration['pipeline_composition']['conf']['project_path'] = self.__path
                configuration['packager']['conf']['project_path'] = self.__path

            self.__build_pipeline.workflow_validator = pf.create(key=configuration['workflow_validation']['type'],
                                                                 configuration=configuration['workflow_validation']['conf'])

            self.__build_pipeline.pipeline_composer = pf.create(key=configuration['pipeline_composition']['type'],
                                                                configuration=configuration['pipeline_composition']['conf'])

            self.__build_pipeline.packager = pf.create(key=configuration['packager']['type'],
                                                       configuration=configuration['packager']['conf'])

            self.__build_pipeline.deployment_artifact_builder = pf.create(key=configuration['orchestration_artifact_builder']['type'],
                                                                          configuration=configuration['orchestration_artifact_builder']['conf'])

            self.__build_pipeline.deployer = pf.create(key=configuration['orchestration_artifact_deployer']['type'],
                                                       configuration=configuration['orchestration_artifact_deployer']['conf'])
            self._logger.info(f"INFO>>{datetime.now().__str__()}:End method {__name__}.build;")
        except:
            error_message = traceback.format_exc()
            self._logger.exception(error_message)
            raise RuntimeError(error_message)