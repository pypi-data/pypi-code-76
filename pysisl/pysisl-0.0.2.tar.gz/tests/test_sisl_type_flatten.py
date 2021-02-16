# Copyright PA Knowledge Ltd 2021

import unittest
from pysisl.sisl_type_flatten import SISLTypeFlatten, UnsupportedSislType


class SislFlatteningTests(unittest.TestCase):
    def test_basic_sisl_structures(self):
        self.assertEqual({"abc": "stuff"}, SISLTypeFlatten.flatten({"abc": {"type": "str", "value": "stuff"}}))

    def test_bool(self):
        self.assertEqual({"abc": True}, SISLTypeFlatten.flatten({"abc": {"type": "bool", "value": "true"}}))
        self.assertEqual({"abc": False}, SISLTypeFlatten.flatten({"abc": {"type": "bool", "value": "false"}}))
        self.assertRaises(UnsupportedSislType, SISLTypeFlatten.flatten, {"abc": {"type": "bool", "value": "eek"}})

    def test_integer(self):
        self.assertEqual({"abc": 1}, SISLTypeFlatten.flatten({"abc": {"type": "int", "value": "1"}}))
        self.assertEqual({"abc": -1}, SISLTypeFlatten.flatten({"abc": {"type": "int", "value": "-1"}}))
        self.assertEqual({"abc": 1000000000000000000000},
                         SISLTypeFlatten.flatten({"abc": {"type": "int", "value": "1000000000000000000000"}}))

    def test_integer_errors_when_decimal_provided(self):
        self.assertRaises(ValueError, SISLTypeFlatten.flatten, {"abc": {"type": "int", "value": "1.1"}})

    def test_integer_errors_if_string(self):
        self.assertRaises(ValueError, SISLTypeFlatten.flatten, {"abc": {"type": "int", "value": "eek"}})

    def test_float(self):
        self.assertEqual({"abc": 1.1}, SISLTypeFlatten.flatten({"abc": {"type": "float", "value": "1.1"}}))
        self.assertEqual({"abc": -1.1}, SISLTypeFlatten.flatten({"abc": {"type": "float", "value": "-1.1"}}))
        self.assertEqual({"abc": 1}, SISLTypeFlatten.flatten({"abc": {"type": "float", "value": "1.0"}}))
        self.assertEqual({"abc": 1}, SISLTypeFlatten.flatten({"abc": {"type": "float", "value": "1"}}))

    def test_empty_list(self):
        self.assertEqual({"abc": []}, SISLTypeFlatten.flatten({"abc": {"type": "list", "value": {}}}))

    def test_single_element_list(self):
        self.assertEqual({"abc": [1]}, SISLTypeFlatten.flatten({"abc": {"type": "list", "value": {"_0": {"type": "int", "value": "1"}}}}))

    def test_two_element_list(self):
        self.assertEqual({"abc": [1, 5]}, SISLTypeFlatten.flatten(
            {"abc": {"type": "list", "value": {
                "_0": {"type": "int", "value": "1"},
                "_1": {"type": "int", "value": "5"}
            }}}))

    def test_nested_list(self):
        self.assertEqual({"abc": [1, [2, "a"]]}, SISLTypeFlatten.flatten(
            {"abc": {"type": "list", "value": {
                "_0": {"type": "int", "value": "1"},
                "_1": {"type": "list", "value": {"_0": {"type": "int", "value": "2"},
                                                 "_1": {"type": "str", "value": "a"}}}}}}))
        self.assertEqual({"abc": [1, [2, {"abc": 4}, {"fgh": [2, 3, 4, 5]}]]}, SISLTypeFlatten.flatten(
            {"abc": {"type": "list", "value": {
                "_0": {"type": "int", "value": "1"},
                "_1": {"type": "list", "value": {"_0": {"type": "int", "value": "2"},
                                                 "_1": {"type": "obj", "value": {"abc": {"type": "int", "value": "4"}}},
                                                 "_2": {"type": "obj", "value": {"fgh": {"type": "list", "value": {
                                                     "_0": {"type": "int", "value": "2"},
                                                     "_1": {"type": "int", "value": "3"},
                                                     "_2": {"type": "int", "value": "4"},
                                                     "_3": {"type": "int", "value": "5"}}}}}}}}}}))

    def test_none_type(self):
        self.assertEqual({"abc": None}, SISLTypeFlatten.flatten({"abc": {"type": "null", "value": ""}}))

    def test_float_errors_if_string(self):
        self.assertRaises(ValueError, SISLTypeFlatten.flatten, {"abc": {"type": "float", "value": "eek"}})

    def test_unsupported_type_does_nothing(self):
        self.assertEqual({"_abc": {"type": "not_supported", "value": "value"}},
                         SISLTypeFlatten.flatten({"_abc": {"type": "not_supported", "value": "value"}}))

    def test_nested_sisl_structures(self):
        self.assertEqual({"abc": {"def": "value"}},
                         SISLTypeFlatten.flatten(
                             {"abc": {"type": "obj", "value": {"def": {"type": "str", "value": "value"}}}}))

    def test_backslash_and_quotes_escaped(self):
        self.assertEqual({"key1": r'some string \ " message'},
                         SISLTypeFlatten.flatten({"key1": {"type": "str", "value": r'some string \\ \" message'}}))


if __name__ == '__main__':
    unittest.main()
