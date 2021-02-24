from enum import Enum, unique


@unique
class AccessMode(Enum):
    SINGLE = "single"
    RECURRENT = "recurrent"
