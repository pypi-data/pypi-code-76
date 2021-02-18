from .DataExporter import DataExporter
import sys

if not ("pyarrow" in sys.modules and "numpy" in sys.modules):
    raise Exception(
        "The default ObjectExporter needs pyarrow numpy to be installed. Try to use 'pip install pyarrow numpy' or use a diffrent exporter"
    )

import pyarrow
import numpy


class ObjectExporter(DataExporter):
    supportedTypes = []

    """ An Exporter that supports a lot of default formats using pyarrow"""

    def checkType(self, type):
        return type in (str, int, bool, float, list, numpy.ndarray) or type in self.supportedTypes
        # TODO: more generic with ?!

    def importData(self, byteString, options={}):
        context = pyarrow.default_serialization_context()
        buffer = pyarrow.py_buffer(byteString)
        df = context.deserialize(buffer)

        return df

    def export(self, df, options={}):
        context = pyarrow.default_serialization_context()
        serialized_df = context.serialize(df)
        buffer = serialized_df.to_buffer()
        byteString = buffer.to_pybytes()

        return byteString
