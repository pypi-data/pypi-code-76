from .base_datatype_mapper import BaseDatatypeMapper

class DictMapper(BaseDatatypeMapper):
    """A Mapper class for Dicts

    This mapper is typically used with the ``Map`` datatype. DynamoDB requires all nested
    values to also match their DynamoDB format when making requests. This class uses
    a ``MapGuesser`` and ``ParseGuesser`` to decide how to resolve and 
    reconstruct each key/value pair.

    Attributes:
        datatype: a DynamoDataType object the mapper is used with
        condition_type: The condition_type of the datatype
        map_guesser: a MapGuesser object, typically associated with the datatype
        parse_guesser: A ParseGuesser object, typically associated with the datatype

    For example::

        mapper = DictMapper(
            DynamoDataType(condition_type="M"),
            DefaultMapGuesser(),
            DefaultParseGuesser())

        mapper.map({
            "email": "test@test.com",
            "number": 123,
        })
        {
            "M": {
                "email": {
                    "S": "test@test.com"
                },
                "number": {
                    "N": "123"
                }
            }
        }


        mapper.reconstruct({"M": {"email": {"S": "test@test.com"}}})
        {
            "email": "test@test.com",
        }
    """
    def __init__(self, datatype, map_guesser, parse_guesser):
        """constructor for the DictMapper

        Parameters:
           datatype: a DynamoDataType object the mapper is used with
           map_guesser: a MapGuesser object, typically associated with the datatype
           parse_guesser: A ParseGuesser object, typically associated with the datatype
        """
        super(DictMapper, self).__init__(datatype)
        self.map_guesser = map_guesser
        self.parse_guesser = parse_guesser

    def resolve(self, value):
        """convert the value into a DynamoDB formatted dictionary

        Use the MapGuesser to find the datatype Use the datatype's mapper to resolve
        the value

        Parameters:
            value: a dict

        Returns:
            a dict converted from the argument into a DynamoDB formatted dictionary
        """
        res = {}
        for key, val in value.items():
            guessed_dt = self.map_guesser.guess(key, val)
            res[key] = guessed_dt.mapper.map(val)
        return res

    def parse(self, value):
        """convert a DynamoDB formatted dict into a single value

        Use the ParseGuesser to find the datatype. Use the datatype's reconstructor to
        parse the value

        Parameters:
            value: a DynamoDB formatted dictionary

        Returns:
            a single value of DynamoDB formatted dict. The value is
            reconstructed based on the guessed datatype of the `ParseGuesser`
        """
        res = {}
        for key, nested_dict in value.items():
            guessed_dt = self.parse_guesser.guess(key, nested_dict)
            res[key] = guessed_dt.mapper.reconstruct(nested_dict)
        return res
