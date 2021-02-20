from .base_datatype_mapper import BaseDatatypeMapper

class StringMapper(BaseDatatypeMapper):
    """A Mapper class for converting string fields into DynamoDB strings

    For example::

        mapper = StringMapper(String())
        mapper.map("hello world")
        {'S': "hello world"}

        mapper.reconstruct({'S': "hello world"})
        "hello world"
    """
    
    def resolve(self, value):
        return str(value)

    def parse(self, value):
        return str(value)
