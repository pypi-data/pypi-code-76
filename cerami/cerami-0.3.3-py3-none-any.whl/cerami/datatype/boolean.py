from .base_datatype import DynamoDataType
from .mapper.boolean_mapper import BooleanMapper

class Boolean(DynamoDataType):
    """A class for Boolean datatypes"""

    def __init__(self, mapper_cls=BooleanMapper, default=None, column_name=""):
        """constructor for the Boolean datatype

        Parameters:
            default: a default value for the column. It can be a value or function
            column_name: a string defining the name of the column on the table
            mapper_cls: A mapper class to manipulate data to/from dynamodb.
                Defaults to the BooleanMapper
        """
        super(Boolean, self).__init__(
            mapper_cls=mapper_cls,
            condition_type="BOOL",
            default=default,
            column_name=column_name)
