from datetime import date

from cbrlib.model.NumberObject import NumberObject
from cbrlib.utils.time import date_to_unixtimestamp


class DateObject(NumberObject):

    def __init__(self, value: date):
        super(DateObject, self).__init__(value)

    def to_float(self):
        return float(date_to_unixtimestamp(self.get_value()))
