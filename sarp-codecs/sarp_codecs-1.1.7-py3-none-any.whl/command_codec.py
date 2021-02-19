"""
Codec format for commands
"""

from sarp_codecs.codec import Codec
from collections import OrderedDict

# Map of all channel names to data types. For more info see:
# https://docs.python.org/3/library/struct.html#struct-format-strings
# h = short
# ? = _Bool
msg_schema = OrderedDict([
    ("fc_command", "h"),
    ("fc_soft_armed", "?")
])


class RelayCommandCodec(Codec):
    def __init__(self):
        super(RelayCommandCodec, self).__init__(msg_schema)
