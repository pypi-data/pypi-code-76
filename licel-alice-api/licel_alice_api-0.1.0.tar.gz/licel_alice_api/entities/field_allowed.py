from enum import Enum

from ..utils import DictWrapper, dict_prop


class FieldAllowedType(Enum):
    STRING = "String"
    BOOLEAN = "Boolean"
    NUMBER = "Integer"
    DATE_TIME = "LocalDateTime"


class FieldAllowed(DictWrapper):
    long_name: str = dict_prop()
    short_name: str = dict_prop()
    type: FieldAllowedType = dict_prop(wrapper=FieldAllowedType)
