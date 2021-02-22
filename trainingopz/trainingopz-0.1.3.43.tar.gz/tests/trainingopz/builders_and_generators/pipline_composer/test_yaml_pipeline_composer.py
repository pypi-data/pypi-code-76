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
from trainingopz.builders_and_generators.pipline_composer.yaml_pipeline_composer import YAMLPipelineComposer
from trainingopz.exceptions.flow_build_error import FlowBuildError
from trainingopz.exceptions.pipeline_read_error import PipelineReadError
from unittest import TestCase
import os


class TestYAMLPipelineComposer(TestCase):

    def setUp(self) -> None:
        config = dict(
            project_path=os.path.abspath('./tests/ml_qookeys')
        )

        self.__yaml_pipeline_composer = YAMLPipelineComposer(**config)

    def tearDown(self) -> None:
        pass

    def test_build_part(self):
        """ Due to _build is not implemented in PipelineComposer it raised NotImplement error not FlowError """

        val_in = {
            'workflows': {
                'pipelines': []
            }
        }
        with self.assertRaises(FlowBuildError):
            self.__yaml_pipeline_composer.build_part(**val_in)

    def test_build(self):

        val_in = {
            'pipelines': [{
                'name': 'test_pipeline',
                'active': True

            }]
        }
        with self.assertRaises(RuntimeError):
            self.__yaml_pipeline_composer._build(val_in)

