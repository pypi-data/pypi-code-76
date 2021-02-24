from enum import Enum, unique


@unique
class FieldType(Enum):
    Int = 0
    Float = 1
    String = 2
    Bool = 3
    Array = 4
    Object = 5
    File = 6
