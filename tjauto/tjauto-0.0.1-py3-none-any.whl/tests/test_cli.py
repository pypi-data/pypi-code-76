import unittest
import os
from tjauto import cli_util

class TestCli(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.system("rm ./tests/assets/cli/NEW_FILE")

    def test_goto_and_exec(self):
        self.assertTrue( not os.path.exists("./tests/assets/cli/NEW_FILE"))
        cli_util.goto_and_exec("./tests/assets/cli","touch NEW_FILE")
        self.assertTrue( os.path.exists("./tests/assets/cli/NEW_FILE"))
