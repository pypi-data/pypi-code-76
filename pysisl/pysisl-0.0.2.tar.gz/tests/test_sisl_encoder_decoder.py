# Copyright PA Knowledge Ltd 2021

import unittest
from pysisl.sisl_encoder import SislEncoder
from pysisl.sisl_decoder import SislDecoder


class SislEncoderDecoderTests(unittest.TestCase):
    def test_basic_dict_structure(self):
        encoder_input = {}
        self.assertEqual(encoder_input, SislDecoder().loads(SislEncoder.dumps(encoder_input)))

    def test_string_values(self):
        encoder_input = {"field_one": "string"}
        self.assertEqual(encoder_input, SislDecoder().loads(SislEncoder.dumps(encoder_input)))

    def test_multiple_nested_dict(self):
        encoder_input = {"field_one": {"field_two": 123, "field_three": {"field_four": "field_four string"}}}
        self.assertEqual(encoder_input, SislDecoder().loads(SislEncoder.dumps(encoder_input)))

    def test_float_values(self):
        encoder_input = {"field_one": 1.0}
        self.assertEqual(encoder_input, SislDecoder().loads(SislEncoder.dumps(encoder_input)))

    def test_nested_list(self):
        encoder_input = {"field_one": [1, [2, 3]]}
        self.assertEqual(encoder_input, SislDecoder().loads(SislEncoder.dumps(encoder_input)))


if __name__ == '__main__':
    unittest.main()
