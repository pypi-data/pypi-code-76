from .base_datatype_mapper import BaseDatatypeMapper

class BooleanMapper(BaseDatatypeMapper):
    """A Mapper class for converting fields into DynamoDB booleans

    For example::
    
        mapper = BooleanMapper(Boolean())
        mapper.map(True)
        {'BOOL': True}

        mapper.reconstruct({'BOOL': True})
        True
    """

    def resolve(self, value):
        return bool(value)

    def parse(self, value):
        return bool(value)
