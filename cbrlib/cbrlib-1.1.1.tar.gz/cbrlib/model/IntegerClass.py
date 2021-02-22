import datetime

from cbrlib.model.IntegerObject import IntegerObject
from cbrlib.model.ModelObject import ModelObject
from cbrlib.model.NumberClass import NumberClass
from cbrlib.utils.time import date_to_unixtimestamp, datetime_to_unixtimestamp


class IntegerClass(NumberClass):

    def __init__(self, id_: str):
        super(IntegerClass, self).__init__(id_)

    def get_typename(self) -> str:
        return 'integer'

    def create_object(self, value: object) -> ModelObject:
        if isinstance(value, (str, float)):
            return IntegerObject(int(value))
        if isinstance(value, datetime.datetime):
            return IntegerObject(datetime_to_unixtimestamp(value))
        if isinstance(value, datetime.date):
            return IntegerObject(date_to_unixtimestamp(value))
        if not isinstance(value, int):
            raise ValueError('Argument must be of type "int".')
        return IntegerObject(value)
