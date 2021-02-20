from .base_datatype_mapper import BaseDatatypeMapper

class IntegerMapper(BaseDatatypeMapper):
    """A Mapper class for converting number fields into DynamoDB dictionaries

    It rounds down to convert any number into an integer

    For example::

        mapper = IntegerMapper(Number())
        mapper.map(30.6)
        {'N': '30'}

        mapper.reconstruct({'N': '30'})
        30
    """
    def resolve(self, value):
        """convert the number into a string"""
        return str(int(value))

    def parse(self, value):
        """convert the value into an int"""
        return int(value)

