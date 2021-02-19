import os

class ResourceReader(object):

    @staticmethod
    def getResourceContent(fileName):
        resourceFilePath = ResourceReader.getResourcePath(fileName)

        with open(resourceFilePath, 'r') as file:
            return file.read()

    @staticmethod
    def getResourcePath(fileName):
        localDirectory = os.path.dirname(__file__)
        return os.path.join(localDirectory, fileName)
