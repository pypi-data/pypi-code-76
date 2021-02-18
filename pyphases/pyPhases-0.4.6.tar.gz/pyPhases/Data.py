import re
from pyPhases import Project
from pyPhases.util.Logger import classLogger
from pyPhases.util.Optionizable import Optionizable


class DataNotFound(Exception):
    pass


class Data(Optionizable):
    project: Project
    dataNames = {}
    version = "current"

    def flattenDict(self, o: dict) -> str:
        values = o.values()
        return self.flatten(list(values))

    def flattenArray(self, o: list, seperator="_") -> str:
        r = []
        for v in o:
            r.append(self.flatten(v))

        return seperator.join(r)

    def flatten(self, o) -> str:
        if isinstance(o, dict):
            return self.flattenDict(o)
        if isinstance(o, list):
            return self.flattenArray(o)

        return None if o is None else re.sub("[^a-zA-Z0-9 ]", "-", str(o))

    @staticmethod
    def flattenConfigValues(o):
        return Data("").flatten(o)

    def __init__(self, name, dataTags=[]):
        self.name = name
        self.dataTags = dataTags
        Data.dataNames[name] = self

    def _getTagValue(self, tagname):
        # TODO: circle detection
        if tagname in Data.dataNames:
            tags = Data.dataNames[tagname].dataTags
            self.logDebug("Data %s depends on different dataset %s: %s" % (self.name, tagname, tags))
            return self.parseDatanames(Data.dataNames[tagname].dataTags)
        return self.flatten(self.project.getConfig(tagname))

    def setProject(self, project):
        self.project = project

    def parseDatanames(self, tags):
        tagList = map(self._getTagValue, tags)
        return "-".join([t for t in tagList if t is not None])

    def getTagString(self):
        return self.parseDatanames(self.dataTags)

    def getDataName(self):
        return self.name + self.getTagString()

    def __str__(self):
        return self.getDataName()

    def getDataId(self):
        return self.getDataName() + "--" + self.version

    @staticmethod
    def create(val, project):
        dataObj = None
        if isinstance(val, Data):
            dataObj = val
        elif isinstance(val, str):
            dataObj = Data(val)
        else:
            raise Exception("Unsupported type as data identifier")

        dataObj.setProject(project)

        return dataObj

    @staticmethod
    def getFromName(name):
        if not name in Data.dataNames:
            raise Exception("The DataWrapper with name %s was not defined and does not exist in any phase" % (name))
        return Data.dataNames[name]
