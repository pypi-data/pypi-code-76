# from .Phase import Phase
from typing import Dict
from pyPhases.storage.Storage import Storage
from pyPhases.Data import Data, DataNotFound
from pyPhases.Stage import Stage
from pyPhases.Phase import Phase
from pyPhases.decorator.ExportValidator import ExportValidator
from pyPhases.util.Logger import Logger
from pyPhases.util.Optionizable import Optionizable
from pyPhases.util.EventBus import EventBus


class ConfigNotFoundException(Exception):
    pass


class Project(Optionizable, EventBus):
    """
    Represents a whole project with several phases

    Parameters
    ----------
    name : string
        name of the project
    namespace : string
        namespace of the project e.e tud.ibmt
    dataStorage : storage
        the storage engine that should be used for storing all kinds of data
        (the default is a Filestorage pointing to the data/ directory)
    """

    def __init__(self):
        self.phases = {}
        self.name = "myProject"
        self.namespace = ""
        self.stages = []
        self.classes = []
        self.exporters = []
        self.classesMap = {}
        self.registeredData = {}
        self.config = {}
        self.dataStorage = []
        self.stageIndex = 0
        self.phaseIndex = 0
        self.decorators = []
        self.debug = False
        self.testRun = False
        self.phaseMap = {}
        self.logLevel = None
        self.gridOutput = None
        self.registerDecorator(ExportValidator())

    def addStorage(self, storage):
        self.logDebug("Add StorageHandler: " + type(storage).__name__)
        self.dataStorage.append(storage)

    def registerDecorator(self, decorator):
        self.logDebug("Register Decorator: " + type(decorator).__name__)
        self.decorators.append(decorator)

    def registerPublisher(self, publisher):
        self.logDebug("Register Publisher: " + type(publisher).__name__)
        self.registerDecorator(publisher)

    def registerExporter(self, exporter):
        self.logDebug("Register Exporter: " + type(exporter).__name__)
        self.exporters.append(exporter)

    def setClasses(self, classes):
        self.classes = classes
        for index, className in enumerate(self.classes):
            self.classesMap[className] = index

    def addStage(self, stageName: str, autorun=True):
        """creates a stage for the project, a stage is a sequential list of phases
        Parameters
        ----------
        stageName : str
            a unique name of the stage that should be created
        """
        stage = Stage(stageName, {"autorun": autorun})
        self.stages += [stage]
        self.phases[stageName] = []

    def getExporterForIntsance(self, instance):
        self.logDebug("Get Exporter For: " + type(instance).__name__)
        return self.getExporterForType(type(instance))

    def getExporterForType(self, theType, storage: Storage = None, reinit=True):
        exporters = self.exporters

        if theType is None:
            return None

        if storage != None and storage.acceptedExporter != None:
            exporters = storage.acceptedExporter

        for exporter in exporters:
            self.logDebug("Check: " + type(exporter).__name__)
            if exporter.checkType(theType):
                self.logDebug("Found exporter")
                if reinit:
                    return exporter.reinit()
                else:
                    return exporter
        return None

    def getDataFromName(self, dataName: str, version: str = "current"):

        dataObj = Data.getFromName(dataName)
        dataObj.version = version
        dataObj.setProject(self)

        return dataObj

    def registerStream(self, dataName, expectedReturnType, options, version: str = "current"):
        dataObj = self.getDataFromName(dataName, version=version)
        dataId = dataObj.getDataId()

        exporter = self.getExporterForType(expectedReturnType)
        if exporter is None:
            raise Exception("No stream exporter found for type %s" % (expectedReturnType))
        return exporter.stream(dataId, options)

    def getExporterAndId(self, dataName, expectedReturnType, options={}, version: str = "current"):

        dataObj = self.getDataFromName(dataName, version=version)
        dataId = dataObj.getDataId()

        try:
            exporter = self.getExporterForType(expectedReturnType, reinit=False)
            return exporter, dataId
        except Exception:
            raise Exception("No stream exporter found for this")

    def dataExists(self, data: Data):
        return data.getDataId() in self.registeredData

    def getExporterObject(self, dataId: str, expectedReturnType=None):

        self.logDebug("Try to get Data: " + dataId)

        for storage in self.dataStorage:
            self.logDebug("Check storage: " + type(storage).__name__)
            exporter = self.getExporterForType(expectedReturnType, storage)
            if exporter is None:
                raise Exception("No exporter found for this type: %s" % (expectedReturnType))

            if exporter.includesStorage:
                return exporter
            return exporter

        exporter = self.getExporterForType(expectedReturnType)
        if exporter != None and exporter.includesStorage:
            return exporter
        return None

    def dataStored(self, dataName: str, expectedReturnType=None, version: str = "current", options={}):
        dataObj = self.getDataFromName(dataName, version=version)
        dataId = dataObj.getDataId()

        exporter = self.getExporterObject(dataId, expectedReturnType)

        return exporter.exists(dataId)

    def getData(self, dataName: str, expectedReturnType=None, version: str = "current", options={}, generate=True):

        dataObj = self.getDataFromName(dataName, version=version)
        dataId = dataObj.getDataId()

        self.logDebug("Try to get Data: " + dataId)

        # just generated Data
        if dataId in self.registeredData:
            self.logDebug("Data in memory: " + dataId)
            return self.registeredData[dataId]

        # load from storage layer
        try:
            for storage in self.dataStorage:
                self.logDebug("Check storage: " + type(storage).__name__)
                exporter = self.getExporterForType(expectedReturnType, storage)
                if exporter is None:
                    self.logWarning("No exporter found for this type: %s" % (expectedReturnType))
                    raise DataNotFound()

                if exporter.includesStorage:
                    return exporter.importData(dataId, options)

                dataBytes = storage.read(dataId)
                self.logDebug("Data in storage: " + type(storage).__name__)
                return exporter.importData(dataBytes, options)

            exporter = self.getExporterForType(expectedReturnType)
            if exporter != None and exporter.includesStorage:
                return exporter.importData(dataId, options)

        except DataNotFound:
            pass

        # regenerate from previous stage/s
        if generate and version == "current":
            self.logWarning("Data " + dataId + " was not found, rerunning previous stages for current data")

            for phase in self.getPhases():
                if dataName in phase.exportDataStrings:
                    phase.getData(dataName)
                    return self.getData(dataName, expectedReturnType, version, options)

        raise DataNotFound("Data " + dataName + " was not found")

    def registerData(self, dataName: str, data: str, version: str = "current", save: bool = True):

        dataObj = self.getDataFromName(dataName, version=version)
        dataId = dataObj.getDataId()

        # save to runtime project
        self.registeredData[dataId] = data

        if save == False:
            return

        if self.dataStorage == None:
            self.logWarning("There was no datastorage registerd")
            return

        # save to storage layer
        exporter = self.getExporterForIntsance(data)

        if exporter == None:
            self.logWarning(
                "No exporter for datatype (" + type(data).__name__ + ") the data " + dataName + " will not be automaticly save"
            )
            return

        if exporter.includesStorage:
            exporter.exportDataId(dataId, data)
        else:
            dataBytes = exporter.export(data, dataId)
            for storage in self.dataStorage:
                storage.write(dataId, dataBytes)

    def setConfig(self, name: str, value):
        self.config[name] = value

    def getConfig(self, name: str) -> str:
        if not name in self.config:
            raise ConfigNotFoundException(
                "The Config entry '%s' was not found, if you rely on a earlier config entry in a previous phase make sure you put the config entry in the __init__ section of the phase"
                % (name)
            )
        return self.config[name]

    def addConfig(self, config) -> None:
        for name in config:
            if name in self.config:
                Warning("The config name " + name + " was specified in multiple phases and was overwritten by the latest!")

            self.config[name] = config[name]

    def addPhase(self, phase, stage: str = "default", name: str = None):
        if name != None:
            phase.name = name

        self.addConfig(phase.config)
        phase.project = self

        if not stage in self.phases:
            self.addStage(stage)

        self.phaseMap[type(phase).__name__] = phase
        self.phases[stage] += [phase]
        phase.prepare()

    def resetConfg(self):
        self.log("Reset Config")
        for index in self.phaseMap:
            phase = self.phaseMap[index]
            phase._prepared = False
            phase.prepare()

    def runAllStages(self):
        for stage in self.stages:
            if stage.getOption("autorun"):
                self.runStage(stage.name)

    def runStage(self, stageName):
        self.log("RUN stage " + stageName)
        for phase in self.phases[stageName]:
            self.runPhase(phase)

    def runStageOrPhase(self, stageOrPhaseName):
        if stageOrPhaseName in self.stages:
            self.runStage(stageOrPhaseName)
        else:
            phase = self.getPhase(stageOrPhaseName)
            self.runPhase(phase)

    def run(self, stageOrPhaseName=None):
        if self.logLevel is not None:
            Logger.verboseLevel = self.logLevel

        if stageOrPhaseName == None:
            self.runAllStages()
        else:
            self.runStageOrPhase(stageOrPhaseName)

        self.trigger("afterRun")

    def runPhase(self, phase: Phase):
        phase.run()

    def getPhase(self, name: str) -> Phase:
        return self.phaseMap[name]

    def getPhases(self):
        for stage in self.stages:
            for phase in self.phases[stage.name]:
                yield phase
