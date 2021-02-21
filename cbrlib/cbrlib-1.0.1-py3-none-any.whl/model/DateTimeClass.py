from datetime import date, datetime

from cbrlib.model import ModelObject
from cbrlib.model.DateTimeObject import DateTimeObject
from cbrlib.model.NumberClass import NumberClass
from cbrlib.utils.time import date_to_datetime


class DateTimeClass(NumberClass):

    def __init__(self, id_: str):
        super(DateTimeClass, self).__init__(id_)

    def get_typename(self) -> str:
        return 'datetime'

    def create_object(self, value: object) -> ModelObject:
        if isinstance(value, str):
            return DateTimeObject(datetime.fromisoformat(value))
        if isinstance(value, int):
            return DateTimeObject(datetime.fromtimestamp(float(value) / 1000))
        if isinstance(value, float):
            return DateTimeObject(datetime.fromtimestamp(value / 1000))
        if not isinstance(value, datetime):
            if isinstance(value, date):
                return DateTimeObject(date_to_datetime(value))
            raise ValueError('Argument must be of type "datetime".')
        return DateTimeObject(value)
