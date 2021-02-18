import unittest
from tjauto import json_util

class TestJSON(unittest.TestCase):
    def test_read_json_file_has_array(self):
        json_data = json_util.read_json_file("./tests/assets/json/string_array.json")
        self.assertEqual(json_data, ['a','b'])
    def test_read_json_file_has_object(self):
        json_data = json_util.read_json_file("./tests/assets/json/object.json")
        self.assertEqual(json_data, {"name": "T,J", "phones": ["1234567890", "0987654321"]})


if __name__ == '__main__':
    unittest.main()