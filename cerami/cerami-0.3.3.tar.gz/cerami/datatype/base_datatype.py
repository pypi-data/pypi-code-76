from .expression import (
    EqualityExpression,
    InExpression)

class DynamoDataType(object):
    """Abstract class for all DataTypes

    A DynamoDataType defines a column on the Model. They should be classlevel attributes
    that are used build models and supplement any sort of Request performed on the table.
    This is the base class for all datatypes and defines many shared expressions used by
    all of the different child classes.
    """

    def __init__(self, default=None, column_name="", condition_type="", mapper_cls=None):
        """Constructor for DynamoDataType

        Parameters:
            default: a default value for the column. It can be a value or function
            column_name: a string defining the name of the column on the table
            mapper_cls: A Mapper class used to interpret/parse data to/from DynamoDB
            condition_type: A string representing one of the types defined by
                DynamoDB for how the data is stored in the database. While DynamoDB
                supports different datatypes, they are all represented by the following:

                ====  ===============
                ====  ===============
                N     All number types
                S     All string types
                B     ByteBuffer / Binary
                BOOL  Booleans
                SS    A set of Strings
                NS    A set of Numbers
                BS    A set of ByteBuffers
                L     Lists of any datatypes
                M     Maps of key/values
                ====  ===============

        """
        self.default = default
        self.set_column_name(column_name)
        self.condition_type = condition_type
        self.mapper = mapper_cls(self) if mapper_cls else None

    def __eq__(self, value):
        return EqualityExpression('=', self, value)

    def __ne__(self, value):
        return EqualityExpression('<>', self, value)

    def __lt__(self, value):
        return EqualityExpression('<', self, value)

    def __le__(self, value):
        return EqualityExpression('<=', self, value)

    def __gt__(self, value):
        return EqualityExpression('>', self, value)

    def __ge__(self, value):
        return EqualityExpression('>=', self, value)

    def in_(self, *values):
        """Build an InExpression

        InExpressions can only be used with filter() on the model, it cannot be part of
        a KeyConditionExpression. The will filter for the table for values that match
        exactly any of the values passed in as arguments

        Parameters:
            values: anything value to use to filter the table

        Returns:
            An InExpression

        For example::

           Person.scan.filter(Person.name.in_("Mom", "Dad")) 
        """
        return InExpression(self, values)

    def set_column_name(self, val):
        """Update the column_name of this instance

        Parameters:
            value: a string for the new column name
        """
        self.column_name = val

    def build(self, val):
        """build the column value based on the val passed in

        building is called automatically by the DynamoDataAttribute
        when the model is initialized. It will use the default value when present if
        the val passed in is None

        Parameters:
            val: A value that will be used to build the attribute on the instance

        Returns:
            The passed in val or the default when the default is set
        """
        if val is None:
            return self._get_default(val)
        return val

    def _get_default(self, val=None):
        """get the default value from the datatype"""
        if self.default is not None:
            if callable(self.default):
                return self.default()
            else:
                return self.default
        return None
