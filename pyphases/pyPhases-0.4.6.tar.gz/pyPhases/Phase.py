import os
from pyPhases import Project
from pyPhases.util.Optionizable import Optionizable
from pyPhases.Data import Data


class Phase(Optionizable):
    name = ""
    config = {}
    metrics = {}
    summary = {}
    inputs = []
    model = None
    runMethod = "main"
    project: Project = None
    decorators = None
    _prepared = False

    def __init__(self, options={}) -> None:
        super().__init__(options)
        self.exportData = []
        self.exportDataStrings = []

    def prepare(self):
        if self._prepared:
            return
        self.logDebug("Prepare phase: " + self.name)
        self.exportData = list(map(lambda s: Data.create(s, self.project), self.exportData))
        self.exportDataStrings = list(map(lambda data: data.name, self.exportData))
        self.prepareConfig()
        self._prepared = True

        phaseName = self.getId()
        if phaseName in self.project.config:
            for index in self.project.config[phaseName]:
                value = self.project.config[phaseName][index]
                self.logDebug("Overwrite Config %s for phase %s with %s" % (index, phaseName, value))
                setattr(self, index, value)

    def prepareConfig(self):
        pass

    def getDecorators(self):
        if not self.decorators == None:
            return self.decorators

        self.decorators = []
        for decorator in self.project.decorators:
            if decorator.filter(self):
                self.decorators.append(decorator)

        return self.decorators

    def getConfig(self, configName):
        return self.project.getConfig(configName)

    def getData(self, name):
        self.run()

    def getId(self):
        return type(self).__name__

    def run(self):
        phaseName = self.getId()
        self.log("RUN phase %s: %s" % (phaseName, self.name))

        def methodNotFound():
            self.logError("The current phase needs the following method defined: " + self.runMethod)

        method = getattr(self, self.runMethod, methodNotFound)
        decorators = self.getDecorators()

        for decorator in decorators:
            decorator.before(self)

        method()

        for decorator in decorators:
            decorator.after(self)
