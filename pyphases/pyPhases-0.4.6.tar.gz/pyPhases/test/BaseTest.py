from pyPhases.Project import Project
from pyPhases.util.Logger import classLogger
import unittest
from pyPhases.Phase import Phase


@classLogger
class TestCase(unittest.TestCase):
    project: Project = None
    phase: Phase = None
    tmpConfig: dict = {}

    def config(self):
        return None

    def getConfig(self, name):
        if name in self.tmpConfig:
            return self.tmpConfig[name]
        return self.phase.project.getConfig(name)

    def setConfig(self, name, value):
        return self.phase.project.setConfig(name, value)

    def getData(self, data):
        return self.phase.project.getData(data)

    def assertDataEqual(self, dataname, value):
        data = self.getData(dataname)
        self.assertEqual(data, value)

    def setProject(self, project):
        self.project = project

    def prepare(self) -> None:
        if self.phase is not None:
            self.phase.project = TestCase.project
        else:
            self.logWarning("TestCase has no Phase connected, might aswell just use TestCase from unittest")

        config = self.config()
        config = {} if config is None else config
        self.phaseConfig = config

        for field in config:
            TestCase.project.setConfig(field, config[field])

        if self.phase is not None:
            self.phase.prepare()

    def tearDown(self) -> None:
        TestCase.project.config = self.restoreConfig

    def setUp(self) -> None:
        self.logDebug("setup phase TestCase")
        self.restoreConfig = TestCase.project.config.copy()
        self.prepare()
