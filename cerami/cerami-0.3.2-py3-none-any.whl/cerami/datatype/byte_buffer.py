from .base_datatype import DynamoDataType
from .mapper import ByteMapper

class ByteBuffer(DynamoDataType):
    """A class for all ByteBuffer and Binary datatypes"""

    def __init__(self, mapper_cls=ByteMapper, default=None, column_name=""):
        """constructor for the ByteBuffer

        Parameters:
            default: a default value for the column. It can be a value or function
            column_name: a string defining the name of the column on the table
            mapper_cls: a mapper class to manipulate data to/from dynamodb.
                Defaults to the ByteMapper
        """
        super(ByteBuffer, self).__init__(
            mapper_cls=mapper_cls,
            condition_type="B",
            default=default,
            column_name=column_name)
