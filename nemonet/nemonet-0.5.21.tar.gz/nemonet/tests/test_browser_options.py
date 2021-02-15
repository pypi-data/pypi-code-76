# Created by Jan Rummens at 12/01/2021
import unittest
from nemonet.runner.vision_runner import Runner

class BrowserOptionsTestCase(unittest.TestCase):


    def test_chrome_options(self):
        runner = Runner(runner_config="runner_config.json")
        runner.execute_scenario("dummy")



if __name__ == '__main__':
    unittest.main()
