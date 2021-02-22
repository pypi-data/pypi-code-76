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
from trainingopz.builders_and_generators.pipline_composer.pipeline_composer import PipelineComposer
from unittest import TestCase


class TestPipelineComposer(TestCase):

    def setUp(self) -> None:

        self.__pipeline_composer = PipelineComposer()

    def tearDown(self) -> None:
        pass

    def test_build_part(self):
        """ Due to _build is not implemented in PipelineComposer it raised NotImplement error not FlowError """

        val_in = {
            'workflows': []
        }
        with self.assertRaises(NotImplementedError):
            self.__pipeline_composer.build_part(**val_in)

    def test_build(self):
        val_in = {
            'workflows': []
        }
        with self.assertRaises(NotImplementedError):
            self.__pipeline_composer._build(val_in)
