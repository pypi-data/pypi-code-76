from abc import abstractmethod
import os.path

from ..util.Optionizable import Optionizable


class PermissionDenied(Exception):
    pass


class Storage(Optionizable):
    acceptedExporter = None

    def __init__(self, options={}):
        if not "basePath" in options:
            options["basePath"] = "."
        super(Storage, self).__init__(options)

    def getPath(self, path):
        basePath = self.getOption("basePath")
        return os.path.normpath(basePath + "/" + path)

    def exists():
        pass

    @abstractmethod
    def read(self, path):
        pass

    @abstractmethod
    def write(self, path, data):
        pass
