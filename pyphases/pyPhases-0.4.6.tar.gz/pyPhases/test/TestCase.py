from pyPhases.Project import Project
from pyPhases.util.Logger import classLogger
import unittest
from pyPhases.Phase import Phase


class ProjectNotSetExeption(Exception):
    pass


@classLogger
class TestCase(unittest.TestCase):
    project: Project = None
    phase: Phase = None
    tmpConfig: dict = {}

    def __init__(self, methodName="runTest"):
        if TestCase.project is None:
            raise ProjectNotSetExeption("There is no Project set in static attribute TestCase.project")
        self.phase.project = TestCase.project
        super().__init__(methodName)
        self.restoreConfig = None

    def config(self):
        return None

    def getConfig(self, name):
        if name in self.tmpConfig:
            return self.tmpConfig[name]
        return self.phase.project.getConfig(name)

    def setConfig(self, name, value):
        self.tmpConfig[name] = value

    def getData(self, data):
        return self.phase.project.getData(data)

    def assertDataEqual(self, dataname, value):
        data = self.getData(dataname)
        self.assertEqual(data, value)

    def prepare(self) -> None:
        self.beforePrepare()
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
        self.restoreConfig = TestCase.project.config.copy()
        self.prepare()

    def beforePrepare(self):
        pass
