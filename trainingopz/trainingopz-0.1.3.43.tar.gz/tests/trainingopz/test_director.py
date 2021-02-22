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

import unittest
from trainingopz.builders_and_generators.director import Director
import pathlib
import os


class TestDirector(unittest.TestCase):
    """
    Test Builder Class
    """

    def setUp(self) -> None:
        self.__path = pathlib.Path(__file__).parent.absolute()
        self._builder = Director(path=os.path.join(self.__path, 'ml_qookeys'))

    def tearDown(self) -> None:
        del self._builder

    def test_build_and_run(self):
        with self.assertRaises(Exception):
            self._builder.build_and_run()