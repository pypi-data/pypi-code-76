from .base_datatype_mapper import BaseDatatypeMapper

class SetMapper(BaseDatatypeMapper):
    """A Mapper class for converting a Set into a DynamoDB dictionary

    For example::

        mapper = SetMapper(StringMapper(String()))
        mapper.map(["hello", "world"])
        {'SS': ['hello', 'world']}

        mapper.reconstruct({'SS': ['hello', 'world']})
        ['hello', 'world']
    """
    def __init__(self, mapper):
        """constructor for SetMapper

        Parameters:
           mapper: a MapperObject that this Set decoratar shall wrap 
        """
        self.mapper = mapper
        self.condition_type = self.mapper.datatype.condition_type + "S"

    def resolve(self, value):
        return [self.mapper.resolve(i) for i in value]

    def parse(self, value):
        return [self.mapper.parse(i) for i in value]
