"""
The template codec format for fill telemetry.
"""
from sarp_codecs.codec import Codec
from collections import OrderedDict

# Map of all channel names to data types. For more info see:
# https://docs.python.org/3/library/struct.html#struct-format-strings
# f = float
# c = char
# h = short
# p = char[]
msg_schema = OrderedDict([
    ("timestamp", "p"),
    ("cpu_temp", "f"),
    ("adc1_c1", "f"),
    ("adc1_c2", "f"),
    ("adc1_c3", "f"),
    ("adc1_c4", "f"),
    ("adc2_c1", "f"),
    ("adc2_c2", "f"),
    ("adc2_c3", "f"),
    ("adc2_c4", "f"),
    ("armed", "c"),
    ("state", "h"),
    ("scr_tag", "p")
])

class FillTelemCodec(Codec):
    def __init__(self):
        super(FillTelemCodec, self).__init__(msg_schema)
