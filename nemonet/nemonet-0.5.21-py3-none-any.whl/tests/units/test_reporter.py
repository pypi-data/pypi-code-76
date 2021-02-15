# Created by Jan Rummens at 19/01/2021
import unittest

from nemonet.engines.reporter import Reporter
import jira

class ReporterTestCase(unittest.TestCase):

    def test_zephyr(self):
        reporter = Reporter()
        try:
            reporter.publish("dummy_zephyr", Reporter.status_failed)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
