# Copyright PA Knowledge Ltd 2021

from . import sisl_decoder
from . import sisl_encoder


def loads(sisl, schema=None):
    return sisl_decoder.SislDecoder().loads(sisl, schema)


def dumps(dict_to_encode):
    return sisl_encoder.SislEncoder.dumps(dict_to_encode)
