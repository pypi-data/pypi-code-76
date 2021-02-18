from unittest import TestCase
from pyPhases import Project, Phase
from pyPhases.exporter import ObjectExporter
from pyPhases.storage import ArrayStorage
# from pyPhases.exporter.ObjectExporter import ObjectExporter
# import pyPhases


class PhaseTest(TestCase):
    # def test_addPhases(self):
    #     self.assertEqual(expected, actual)

    def test_project(self):

        storage = ArrayStorage("data/")

        project = Project()
        project.registerExporter(ObjectExporter())

        project.name = 'myTestProject'
        project.namespace = 'tud.ibmt'

        # stages
        project.addStage('prepareTest')
        project.addStage('test')

        # add filestorage and data exporter
        project.dataStorage = storage

        phase1 = Phase()


