from datetime import datetime, date

from cbrlib.model.ModelClass import ModelClass
from cbrlib.model.ModelObject import ModelObject
from cbrlib.model.StringObject import StringObject


class StringClass(ModelClass):

    def __init__(self, id_):
        super(StringClass, self).__init__(id_)

    def get_typename(self) -> str:
        return 'string'

    def create_object(self, value: object) -> ModelObject:
        if isinstance(value, (int, float)):
            return StringObject(str(value))
        if isinstance(value, (date, datetime)):
            return StringObject(value.isoformat())
        if not isinstance(value, str):
            raise ValueError('Argument must be of type "str".')
        return StringObject(value)
