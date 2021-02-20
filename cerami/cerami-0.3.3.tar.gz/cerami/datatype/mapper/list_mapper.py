from .base_datatype_mapper import BaseDatatypeMapper

class ListMapper(BaseDatatypeMapper):
    """A Mapper class for Lists

    This mapper is typically used with the ``List`` datatype. DynamoDB requires all items
    of a List to also match the DynamoDB format when making requests. This class uses a
    ``MapGuesser`` and a ``ParseGuesser`` to decide how to resolve and reconstruct each
    key/value pair

    Attributes:
        datatype: a DynamoDataType object the mapper is used with
        condition_type: The condition_type of the datatype
        map_guesser: a MapGuesser object, typically associated with the datatype
        parse_guesser: A ParseGuesser object, typically associated with the datatype

    For example::

        mapper = ListMapper(
            DynamoDataType(condition_type="L"),
            DefaultMapGuesser(),
            DefaultParseGuesser())

        mapper.map(["test@test.com", 123])
        {
            "L": [
                {
                    "S": "test@test.com"
                },
                {
                    "N": "123"
                }
            ]
        }

        mapper.reconstruct({'L': [{'S': 'test@test.com'}, {'N': '123'}]})
        ["test@test.com", 123]
    """

    def __init__(self, datatype, map_guesser, parse_guesser):
        """constructor for the ListMapper

        Parameters:
           datatype: a DynamoDataType object the mapper is used with
           map_guesser: a MapGuesser object, typically associated with the datatype
           parse_guesser: A ParseGuesser object, typically associated with the datatype
        """
        super(ListMapper, self).__init__(datatype)
        self.map_guesser = map_guesser
        self.parse_guesser = parse_guesser

    def resolve(self, value):
        """convert the value into a DynamoDB formatted dictionary

        Parameters:
            values: a list

        Returns:
            a list where each item is a DynamoDB formatted dictionary
        """
        res = []
        for idx, val in enumerate(value):
            guessed_dt = self.map_guesser.guess(idx, val)
            res.append(guessed_dt.mapper.resolve(val))
        return res

    def parse(self, value):
        """convert the DynamoDB formatted dict into a list

        Parameters:
            values: an array of DynamoDB formatted dictionaries

        Returns:
            a list where each item is reconstructed from the guessed datatype of the
            ParseGuesser
        """
        res = []
        for idx, val in enumerate(value):
            guessed_dt = self.parse_guesser.guess(idx, val)
            res.append(guessed_dt.mapper.reconstruct(val))
        return res
