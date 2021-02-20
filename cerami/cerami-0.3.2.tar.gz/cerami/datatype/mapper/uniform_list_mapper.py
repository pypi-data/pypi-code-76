from .base_datatype_mapper import BaseDatatypeMapper

class UniformListMapper(BaseDatatypeMapper):
    """A Mapper class for UniformLists

    Unlike the ListMapper, the UniformListMapper does not need to guess which datatype
    each item in the array is.

    For example::

        mapper = UniformListMapper(StringMapper(String()))
        mapper.map(["hello", "world"])
        {
            "L": [
                {
                    "S": "hello"
                },
                {
                    "S": "world"
                }
            ]
        }

        mapper.reconstruct({"L": [{"S": "hello"}, {"S": "world"}]})
        ["hello", "world"]
    """

    def __init__(self, mapper):
        """constructor for UniformListMapper

        Parameters:
            mapper: a BaseDatatypeMapper object
        """
        self.mapper = mapper
        self.condition_type = "L"

    def resolve(self, value):
        return [self.mapper.map(i) for i in value]

    def parse(self, value):
        return [self.mapper.reconstruct(i) for i in value]
