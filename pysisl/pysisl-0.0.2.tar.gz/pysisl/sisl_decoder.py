# Copyright PA Knowledge Ltd 2021

from .sisl_lexer import *
from .sisl_parser import *

import ply.lex as lex
import ply.yacc as yacc

from . import sisl_type_flatten

from jsonschema import validate as json_validator
from jsonschema import FormatChecker, ValidationError


class SislDecoder:
    def __init__(self):
        self.parser = yacc.yacc()
        lex.lex()

    def loads(self, sisl, schema=None):
        flattened_sisl = sisl_type_flatten.SISLTypeFlatten().flatten(self.parse_raw_types(sisl))
        self._verify_schema_if_required(flattened_sisl, schema)
        return flattened_sisl

    @staticmethod
    def _verify_schema_if_required(flattened_sisl, schema):
        if schema is None:
            return

        try:
            json_validator(flattened_sisl, schema=schema, format_checker=FormatChecker())
        except ValidationError as err:
            raise SislValidationError(err)

    def parse_raw_types(self, sisl):
        return self.parser.parse(sisl)


class SislValidationError(Exception):
    pass
