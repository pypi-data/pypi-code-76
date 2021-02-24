# Created by Antonio Di Mariano (antonio.dimariano@gmail.com) at 04/02/2021
from service_configuration_controller.helpers.operation_with_files import write_data_to_json_file
import unittest
import os
class TestWriteData(unittest.TestCase):

    def test_a_create_dir_and_write_data(self):
        filename = '../../configuration/service_configuration.json'
        configuration_file = os.path.abspath(filename)
        ret = write_data_to_json_file(data_to_persit={"data":"ciao"},filename=configuration_file)
        self.assertEqual(ret,1)

    def test_b_create_dir_and_write_data(self):
        filename = '../../configuration/service_configuration.json'
        configuration_file = os.path.abspath(filename)
        ret = write_data_to_json_file(data_to_persit={"data":"ciao2"},filename=configuration_file)
        self.assertEqual(ret,1)
