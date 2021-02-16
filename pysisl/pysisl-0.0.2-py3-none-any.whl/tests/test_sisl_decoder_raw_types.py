# Copyright PA Knowledge Ltd 2021

import unittest
from pysisl.sisl_decoder import SislDecoder
from pysisl.parser_error import ParserError


class SislRawTypesParsingTests(unittest.TestCase):
    def test_parser_error(self):
        self.assertRaises(ParserError, SislDecoder().parse_raw_types, "{")
        self.assertRaises(ParserError, SislDecoder().parse_raw_types, "{1abc: !type \"value\"}")
        self.assertRaises(ParserError, SislDecoder().parse_raw_types, "{abc: type \"value\"}")
        self.assertRaises(ParserError, SislDecoder().parse_raw_types, "{abc: !type \"value}")

    def test_basic_sisl_structures(self):
        self.assertEqual({}, SislDecoder().parse_raw_types("{}"))
        self.assertEqual({"abc": {"type": "type", "value": "value"}}, SislDecoder().parse_raw_types("{abc: !type \"value\"}"))
        self.assertEqual({
            "abc": {
                "type": "type",
                "value": {
                    "nested": {
                        "type": "type",
                        "value": "value"
                    }
                }
            }
        }, SislDecoder().parse_raw_types("{abc: !type {nested: !type \"value\"}}"))

        self.assertEqual({
            "abc": {
                "type": "type",
                "value": {
                    "nested": {
                        "type": "type",
                        "value": {
                            "nested": {
                                "type": "type",
                                "value": "value"
                            }
                        }
                    }
                }
            }
        }, SislDecoder().parse_raw_types("{abc: !type {nested: !type {nested: !type \"value\"}}}"))

    def test_basic_values(self):
        self.assertEqual({"abc": {"type": "type", "value": "value1"}}, SislDecoder().parse_raw_types("{abc: !type \"value1\"}"))
        self.assertEqual({"abc": {"type": "type", "value": "VALUE1"}}, SislDecoder().parse_raw_types("{abc: !type \"VALUE1\"}"))
        self.assertEqual({"abc": {"type": "type", "value": r'val\"ue'}}, SislDecoder().parse_raw_types(r'{abc: !type "val\"ue"}'))
        self.assertEqual({"abc": {"type": "type", "value": r'val\\ue'}}, SislDecoder().parse_raw_types(r'{abc: !type "val\\ue"}'))
        self.assertEqual({"abc": {"type": "type", "value": r'val ue'}}, SislDecoder().parse_raw_types(r'{abc: !type "val ue"}'))

    def test_lists(self):
        self.assertEqual({"abc": {"type": "type", "value": "value"}, "def": {"type": "typeb", "value": "value2"}},
                         SislDecoder().parse_raw_types("{abc: !type \"value\",def: !typeb \"value2\"}"))

        self.assertEqual({"abc": {"type": "type", "value": "value"}, "def": {"type": "typeb", "value": "value2"},
            "ghi": {"type": "typec", "value": "value3"}},
            SislDecoder().parse_raw_types("{abc: !type \"value\",def: !typeb \"value2\",ghi: !typec \"value3\"}"))

    def test_lists_with_whitespace_after_separator(self):
        self.assertEqual({
            "abc": {"type": "type", "value": "value"},
            "def": {"type": "typeb", "value": "value2"}
        }, SislDecoder().parse_raw_types("{abc: !type \"value\", def: !typeb \"value2\"}"))
        self.assertEqual({"abc": {"type": "type", "value": "value"}, "def": {"type": "typeb", "value": "value2"}},
                         SislDecoder().parse_raw_types("{abc: !type \"value\",  def: !typeb \"value2\"}"))

    def test_lists_with_whitespace_before_separator(self):
        self.assertEqual({"abc": {"type": "type", "value": "value"}, "def": {"type": "typeb", "value": "value2"}},
                         SislDecoder().parse_raw_types("{abc: !type \"value\" , def: !typeb \"value2\"}"))

        self.assertEqual({"abc": {"type": "type", "value": "value"}, "def": {"type": "typeb", "value": "value2"}},
                         SislDecoder().parse_raw_types("{abc: !type \"value\" , def: !typeb \"value2\"}"))

    def test_name_special_chars(self):
        self.assertEqual({"_abc": {"type": "type", "value": "value"}}, SislDecoder().parse_raw_types("{_abc: !type \"value\"}"))
        self.assertEqual({"ab_c_": {"type": "type", "value": "value"}}, SislDecoder().parse_raw_types("{ab_c_: !type \"value\"}"))
        self.assertEqual({"ab.c": {"type": "type", "value": "value"}}, SislDecoder().parse_raw_types("{ab.c: !type \"value\"}"))
        self.assertEqual({"ab3c": {"type": "type", "value": "value"}}, SislDecoder().parse_raw_types("{ab3c: !type \"value\"}"))

    def test_type_special_chars(self):
        self.assertEqual({"abc": {"type": "_abc", "value": "value"}}, SislDecoder().parse_raw_types("{abc: !_abc \"value\"}"))
        self.assertEqual({"abc": {"type": "ab_c", "value": "value"}}, SislDecoder().parse_raw_types("{abc: !ab_c \"value\"}"))
        self.assertEqual({"abc": {"type": "ab.c", "value": "value"}}, SislDecoder().parse_raw_types("{abc: !ab.c \"value\"}"))
        self.assertEqual({"abc": {"type": "ab3c", "value": "value"}}, SislDecoder().parse_raw_types("{abc: !ab3c \"value\"}"))

    def test_value_special_chars(self):
        self.assertEqual({"_abc": {"type": "type", "value": "value="}}, SislDecoder().parse_raw_types("{_abc: !type \"value=\"}"))
        self.assertEqual({"_abc": {"type": "type", "value": "value-"}}, SislDecoder().parse_raw_types("{_abc: !type \"value-\"}"))
        self.assertEqual({"_abc": {"type": "type", "value": "value:"}}, SislDecoder().parse_raw_types("{_abc: !type \"value:\"}"))
        self.assertEqual({"_abc": {"type": "type", "value": "value."}}, SislDecoder().parse_raw_types("{_abc: !type \"value.\"}"))
        self.assertEqual({"_abc": {"type": "type", "value": "value+"}}, SislDecoder().parse_raw_types("{_abc: !type \"value+\"}"))
        self.assertEqual({"_abc": {"type": "type", "value": "value@"}}, SislDecoder().parse_raw_types("{_abc: !type \"value@\"}"))
        self.assertEqual({"_abc": {"type": "type", "value": "value'"}}, SislDecoder().parse_raw_types("{_abc: !type \"value'\"}"))
        self.assertEqual({"_abc": {"type": "type", "value": "value!"}}, SislDecoder().parse_raw_types("{_abc: !type \"value!\"}"))

    def test_allow_space(self):
        self.assertEqual({"_abc": {"type": "type", "value": "value"}}, SislDecoder().parse_raw_types("{_abc: !type \"value\"} "))
        self.assertEqual({"_abc": {"type": "type", "value": "value"}}, SislDecoder().parse_raw_types("{ _abc: !type \"value\"}"))
        self.assertEqual({"_abc": {"type": "type", "value": "value"}}, SislDecoder().parse_raw_types("{_abc: !type \"value\" }"))

    def test_illegal_spaces(self):
        self.assertRaises(ParserError, SislDecoder().parse_raw_types, "{abc: !type  \"value\"}")
        self.assertRaises(ParserError, SislDecoder().parse_raw_types, "{abc:  !type \"value\"}")

    def test_allow_quote_followed_by_space_in_value(self):
        self.assertEqual({"_abc": {"type": "type", "value": r'value\" '}}, SislDecoder().parse_raw_types(r'{_abc: !type "value\" " }'))

    def test_example_syslog_sisl(self):
        self.assertEqual({'app-name': {'type': 'string', 'value': 'containerd'},
                          'date': {'type': 'string', 'value': '2019-08-08T13:50:14.170225+01:00'},
                          'host': {'type': 'string', 'value': 'centosvm'},
                          'message': {'type': 'string',
                                      'value': '  time=2020-12-09T16:47:16.358818934Z'}},
                         SislDecoder().parse_raw_types(r'{date: !string "2019-08-08T13:50:14.170225+01:00", host: !string "centosvm", app-name: !string "containerd", message: !string "  time=2020-12-09T16:47:16.358818934Z"}'))


if __name__ == '__main__':
    unittest.main()
