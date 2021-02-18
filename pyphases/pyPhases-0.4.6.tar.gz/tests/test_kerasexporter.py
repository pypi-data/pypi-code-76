from unittest import TestCase
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation
from pyPhases.exporter import KerasExporter


class KerasExporterTest(TestCase):

    def test_kerasSequential(self):
        model = Sequential()
        model.add(Dense(32, input_dim=784))
        model.add(Activation('relu'))

        exporter = KerasExporter()

        self.assertTrue(exporter.checkType(Sequential))

        string = exporter.export(model)

        self.assertEqual(isinstance(string, bytes), True)
        importedModel = exporter.importData(string)

        self.assertIsInstance(importedModel, keras.Model)
        self.assertIsInstance(importedModel, Sequential)




