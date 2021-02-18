from pathlib import Path
from .Storage import Storage
from ..Data import DataNotFound


class FileStorage(Storage):
    def read(self, path):
        try:
            file = open(self.getPath(path), "rb")
            return file.read()
        except FileNotFoundError:
            self.logDebug("Data was not found: %s (%s)" % (path, self.getPath(path)))
            raise DataNotFound("Data was not found: %s" % (path))

    def write(self, path, data):
        if isinstance(data, bytes):
            writeMode = "wb"
        else:
            writeMode = "w"
        file = open(self.getPath(path), writeMode)
        file.write(data)
        file.close()

    def exists(self, dataId):
        return Path(self.getPath(dataId)).is_file()
