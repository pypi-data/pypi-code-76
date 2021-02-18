from ..util.Optionizable import Optionizable

class DataExporter(Optionizable):
    includesStorage: bool = False
    recreate: bool = True

    """Checks an instance, if its type is compatible with the current Exporter
    """
    def checkType(self, check) -> bool:
        """ Checks an instance, if its type is compatible with the current Exporter
        """
        return False

    def importData(self, raw, options = {}):
        """ this methods transforms raw data from the storage into a specific dataformat (defined by the exporter)
        """
        return raw

    def export(self, data, options = {}):

        """ this method transforms a specific data type into a raw data that the storage can save
        """
        return data

    def stream(self, data, options = {}):
        raise Exception("The exporter has no stream method implemented")

    def finishStream(self, dataId):
        pass

    def reinit(self):
        if not self.recreate:
            return self
        return type(self)(self.options)

