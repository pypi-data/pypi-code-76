from unittest import TestCase
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation
from pyPhases.exporter import ObjectExporter
import numpy


class ObjectExporterTest(TestCase):

    def test_ObjectExporter(self):

        dataSet = [
            [5],
            numpy.array([5,2])
        ]

        exporter = ObjectExporter()

        for data in dataSet:
            self.assertEqual(exporter.checkType(data), True)

            string = exporter.export(data)

            self.assertIsInstance(string, str)
            importedModel = exporter.importData(string)

            self.assertIsInstance(importedModel, type(data))




