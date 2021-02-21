from datetime import date, datetime

from cbrlib.model.DateObject import DateObject
from cbrlib.model.ModelObject import ModelObject
from cbrlib.model.NumberClass import NumberClass


class DateClass(NumberClass):

    def __init__(self, id_: str):
        super(DateClass, self).__init__(id_)

    def get_typename(self) -> str:
        return 'date'

    def create_object(self, value: object) -> ModelObject:
        if isinstance(value, str):
            return DateObject(date.fromisoformat(value))
        if isinstance(value, int):
            return DateObject(date.fromtimestamp(float(value) / 1000))
        if isinstance(value, float):
            return DateObject(date.fromtimestamp(value / 1000))
        if isinstance(value, datetime):
            return DateObject(value.date())
        if not isinstance(value, date):
            raise ValueError('Argument must be of type "date".')
        return DateObject(value)
