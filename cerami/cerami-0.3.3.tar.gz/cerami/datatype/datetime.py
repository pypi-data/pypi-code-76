import dateutil.parser
from datetime import datetime, timezone
from .base_string import BaseString
from .mapper import DatetimeMapper

class Datetime(BaseString):
    """A class to represent all Datetime datatypes"""

    def __init__(self, mapper_cls=DatetimeMapper, default=None, column_name=""):
        """constructor for the Datetime

        Parameters:
            default: a default value for the column. It can be a value or function
            column_name: a string defining the name of the column on the table
            mapper_cls: A mapper class to manipulate data to/from dynamodb.
                Defaults to the DatetimeMapper
        """
        super(Datetime, self).__init__(
            mapper_cls=mapper_cls,
            default=default,
            column_name=column_name)
