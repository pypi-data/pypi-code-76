# Copyright PA Knowledge Ltd 2021

import unittest
from pysisl.sisl_decoder import SislDecoder, SislValidationError


class SislParsingTests(unittest.TestCase):
    def test_basic_sisl_structures_successful_parse(self):
        self.assertEqual({"abc": {"results": {"result": 123}}}, SislDecoder().loads("{abc: !obj {results: !obj {result: !int \"123\"}}}"))

    def test_successful_parse_with_schema(self):
        schema = {
            "properties": {
                "field_one": {
                    "type": "string"
                },
                "field_two": {
                    "type": "number"
                }
            }
        }
        self.assertEqual({"field_one": "string", "field_two": 2},
                         SislDecoder().loads("{field_one: !str \"string\", field_two: !int \"2\"}", schema=schema))

    def test_parse_with_schema_fails_throws_error(self):
        schema = {
            "properties": {
                "field_one": {
                    "type": "number"
                },
                "field_two": {
                    "type": "number"
                }
            }
        }
        self.assertRaises(SislValidationError,
                          SislDecoder().loads, "{field_one: !str \"string\", field_two: !int \"2\"}", schema=schema)


if __name__ == '__main__':
    unittest.main()
