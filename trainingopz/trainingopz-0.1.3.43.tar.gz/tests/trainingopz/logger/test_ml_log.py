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
import unittest
from trainingopz.logger.ml_log import MLLog


class TestMLLog(unittest.TestCase):
    """
    Test Logger Class
    """

    def setUp(self) -> None:
        self.lg = MLLog("test", logging.DEBUG, False).logger

    def tearDown(self) -> None:
        del self.lg

    def test_info(self):
        # Todo test case is not completly correct
        self.assertIsNone(self.lg.info("This is info log test"))

    def test_debug(self):
        var = 1
        #Todo test case is not completly correct, need to find other way to test error
        self.assertIsNone(self.lg.debug(f"This is debug test {var}"))
