# from pyPhases.exporter.ObjectExporter import ObjectExporter
# import pyPhases


from pyPhases.test.TestCaseIntegration import TestCaseIntegration
from pyPhases.Project import ConfigNotFoundException
from tests.util.PhaseGenerator import PhaseGenerator
from pyPhases.test.TestCase import TestCase
from unittest.mock import MagicMock


class TestIntegrationTest(TestCaseIntegration):
    beforeRunCheck = False
    afterRunCheck = False
    phase = TestCase.project.phases["default"][0]

    def testExecution(self):
        self.assertEqual(self.phase.mainExecuted, 1)

    def testSingleExecution(self):
        self.assertEqual(self.phase.mainExecuted, 1)

    @staticmethod
    def beforeRun():
        TestIntegrationTest.beforeRunCheck = True
        assert TestIntegrationTest.phase.mainExecuted == 0

    @staticmethod
    def afterRun():
        TestIntegrationTest.afterRunCheck = True
        assert TestIntegrationTest.phase.mainExecuted == 1

    def testRunDecorators(self):
        self.assertTrue(TestIntegrationTest.afterRunCheck)
        self.assertTrue(TestIntegrationTest.beforeRunCheck)
