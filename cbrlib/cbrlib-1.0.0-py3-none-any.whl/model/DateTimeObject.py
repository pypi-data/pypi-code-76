from datetime import datetime

from cbrlib.model.NumberObject import NumberObject
from cbrlib.utils.time import datetime_to_unixtimestamp


class DateTimeObject(NumberObject):

    def __init__(self, value: datetime):
        super(DateTimeObject, self).__init__(value)

    def to_float(self):
        return float(datetime_to_unixtimestamp(self.get_value()))
