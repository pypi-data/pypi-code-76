# Copyright PA Knowledge Ltd 2021

import unittest
from pysisl.sisl_encoder import SislEncoder, TypeValidationError


class NotSislClass:
    def __init__(self):
        self.name = "unknown object"


class SislParsingTests(unittest.TestCase):
    def test_basic_dict_structure_successfully_converted_to_sisl(self):
        self.assertEqual("{}", SislEncoder.dumps({}))

    def test_string_values_successfully_converted_to_sisl(self):
        self.assertEqual("{field_one: !str \"string\"}", SislEncoder.dumps({"field_one": "string"}))
        self.assertEqual("{field_one: !str \"string\", field_two: !str \"string2\"}",
                         SislEncoder.dumps({"field_one": "string", "field_two": "string2"}))

    def test_int_values_successfully_converted_to_sisl(self):
        self.assertEqual("{field_one: !int \"123\"}", SislEncoder.dumps({"field_one": 123}))

    def test_float_values_successfully_converted_to_sisl(self):
        self.assertEqual("{field_one: !float \"1.23\"}", SislEncoder.dumps({"field_one": 1.23}))
        self.assertEqual("{field_one: !float \"-0.123\"}", SislEncoder.dumps({"field_one": -0.123}))
        self.assertEqual("{field_one: !float \"1.0\"}", SislEncoder.dumps({"field_one": 1.0}))

    def test_bool_values_successfully_converted_to_sisl(self):
        self.assertEqual("{field_one: !bool \"true\"}", SislEncoder.dumps({"field_one": True}))
        self.assertEqual("{field_one: !bool \"false\"}", SislEncoder.dumps({"field_one": False}))

    def test_single_element_integer_list_values_successfully_converted_to_sisl(self):
        self.assertEqual("{field_one: !list {_0: !int \"1\"}}", SislEncoder.dumps({"field_one": [1]}))

    def test_list_values_successfully_converted_to_sisl(self):
        self.assertEqual("{field_one: !list {_0: !int \"1\", _1: !int \"2\", _2: !int \"3\"}}", SislEncoder.dumps({"field_one": [1, 2, 3]}))
        self.assertEqual("{field_one: !list {_0: !list {_0: !int \"4\"}, _1: !int \"2\", _2: !int \"3\"}}", SislEncoder.dumps({"field_one": [[4], 2, 3]}))

    def test_basic_nested_dict_structure_successfully_converted_to_sisl(self):
        self.assertEqual("{field_one: !obj {}}", SislEncoder.dumps({"field_one": {}}))

    def test_nested_dict_structure_successfully_converted_to_sisl(self):
        self.assertEqual("{field_one: !obj {field_two: !int \"123\"}}", SislEncoder.dumps({"field_one": {"field_two": 123}}))

    def test_multiple_nested_dict_structure_successfully_converted_to_sisl(self):
        self.assertEqual("{field_one: !obj {field_two: !int \"123\", field_three: !str \"field_three string\"}}",
                         SislEncoder.dumps({"field_one": {"field_two": 123, "field_three": "field_three string"}}))
        self.assertEqual("{field_one: !obj {field_two: !int \"123\", field_three: !obj {field_four: !str \"field_four string\"}}}",
                         SislEncoder.dumps({"field_one": {"field_two": 123, "field_three": {"field_four": "field_four string"}}}))

    def test_unknown_types_in_dictionary_should_throw_error(self):
        self.assertRaises(TypeValidationError, SislEncoder.dumps, {"field_two": NotSislClass()})

    def test_none_type_successfully_converted_to_sisl(self):
        self.assertEqual("{field_one: !null \"\"}", SislEncoder.dumps({"field_one": None}))


if __name__ == '__main__':
    unittest.main()
