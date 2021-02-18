from unittest import TestCase
from pyPhases.storage import ArrayStorage
# from pyPhases.exporter.ObjectExporter import ObjectExporter
# import pyPhases


class PhaseTest(TestCase):
    # def test_addPhases(self):
    #     self.assertEqual(expected, actual)

    def test_readwrite(self):
        testString = "blub"
        arraystorage = ArrayStorage()
        arraystorage.write("my/test/path", testString)
        read = arraystorage.read("my/test/path")
        self.assertEqual(read, testString)

    def test_readwritePathNormalize(self):
        testString = "blub"
        arraystorage = ArrayStorage()
        arraystorage.write("./my/./test/path", testString)
        read = arraystorage.read("./my/test/../test/path")
        self.assertEqual(read, testString)


