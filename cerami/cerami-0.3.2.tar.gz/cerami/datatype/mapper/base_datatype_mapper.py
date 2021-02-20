class BaseDatatypeMapper(object):
    """The base class for all Mappers

    Mappers are responsible for translating between a model's data and DynamoDB. All
    requests need to have the data formatted in a specific way, and all responses from
    DynamoDB are formatted similarly. A Mapper is responsible for converting to and from
    this DynamoDB structure.

    Attributes:
        datatype: a DynamoDataType object the mapper is used with
        condition_type: The condition_type of the datatype

    For example::

        mapper = BaseDatatypeMapper(Person.email)
        mapper.map("test@test.com")
        {
            "S": "test@test.com"
        }

        mapper.reconstruct({"S": "test@test.com"})
        "test@test.com"
    """
    def __init__(self, datatype):
        """constructor for the BaseDatatypeMapper

        Parameters:
            datatype: a DynamoDataType object the mapper is used with
        """
        self.datatype = datatype
        self.condition_type = self.datatype.condition_type

    def map(self, value):
        """return the value and its condition_type

        Mapping is done when converting the model into a form
        readable by DynamoDB. Mapping involves two steps.
        First it must return a dict of the value.
        Second it must "resolve" the value so DynamoDB can process it.

        Parameters:
            value: anything that should be converted into a DynamoDB formatted dict

        Returns:
            a dict in a format expected by DynamoDB. Its key is the condition_type of this
            instance and value the return value of ``resolve()``. It will automatically
            return ``{"NULL": True}`` when the value passed in is ``None``

        For example::

            mapper = BaseDatatypeMapper(Person.email)
            mapper.map("test@test.com")
            {
                "S": "test@test.com"
            }
        """
        if value == None:
            return {'NULL': True}
        res = {}
        res[self.condition_type] = self.resolve(value)
        return res

    def resolve(self, value):
        """returns the value resolved for dynamodb

        This method is called by ``map()`` to convert the value itself into a format
        that is expected for DynamoDB. For example, all Number datatypes need to be
        converted to strings in before being submitted.

        Parameters:
            value: anything that should be converted to a DynamoDB dict by ``map()``

        Returns:
            the value as is. Any child class should override this method to convert the
            value as necessary.
        """
        return value

    def reconstruct(self, mapped_dict):
        """return the value from the mapped dict for model instantiation

        DynamoDB returns all attributes as a dict. Reconstructing reads this dict and
        "parses" the value. The return value can be used as the attribute on the Model.
        Reconstructing is only responsible for parsing the data as-is from DynamoDB. The
        process of assigning default values is done by the datatype itself.

        Parameters:
            mapped_dict: A DynamoDB dictionary, whose key is the condition type of this
                instance and value is what needs to be `parsed`. The key can also be
                ``"NULL"`` which represents null values in DynamoDB

        Returns:
            the parsed value from the `mapped_dict`. It will return ``None`` when the key
            of the mapped_dict is ``"NULL"``.

        For example::

            mapper = BaseDatatypeMapper(Person.email)
            mapper.reconstruct({"S": "test@test.com"})
            "test@test.com"
        """
        if mapped_dict.get('NULL') == True:
            return None
        return self.parse(mapped_dict[self.condition_type])

    def parse(self, value):
        """Convert the value from DynamoDB into a format for the Model

        This is the opposite of resolving. So when given the DynamoDB dict
        ``{"S": "Mom"}`` it will return ``"Mom"``

        Parameters:
            value: anything that should be converted from a DynamoDB dict's value
                value should never be None, reconstruct will not pass it here
        Returns:
            the value as is. All child classes should override this method to convert the
            value however necessary.
        """
        return value
