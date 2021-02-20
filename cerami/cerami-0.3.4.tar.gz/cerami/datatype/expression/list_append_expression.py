from .base_expression import BaseExpression

class ListAppendExpression(BaseExpression):
    """A class to generate list_append expressions for `UpdateRequests`

    When using an `UpdateRequest`, a `ListAppendExpression` can be used for any
    `List` datatype.

    For example::

       # you can use Person.toys.append() instead!
       expression = ListAppendExpression(Person.toys, [{"color": "red", "name": "car"}]) 
       Person.update.key(Person.email == "test@test.com").set(expression).build()
        {
            "TableName": "people",
            "ReturnValues": "ALL_NEW",
            "Key": {
                "email": {
                    "S": "test@test.com"
                }
            },
            "UpdateExpression": "SET #__toys = list_append(#__toys, :_toys_ihkiy)",
            "ExpressionAttributeNames": {
                "#__toys": "toys"
            },
            "ExpressionAttributeValues": {
                ":_toys_ihkiy": {
                    "L": [
                        {
                            "M": {
                                "color": {
                                    "S": "red"
                                },
                                "name": {
                                    "S": "car"
                                }
                            }
                        }
                    ]
                }
            }
        }
    """
    def __init__(self, datatype, value):
        """constructor for ListAppendExpression

        Parameters:
            datatype: a DynamoDataType that the expression is for
            value: a an array to append to the existing datatype column
        """
        super(ListAppendExpression, self).__init__( '=', datatype, value)

    def __str__(self):
        attr_name = self.expression_attribute_name
        if hasattr(self.datatype, '_index'):
            attr_name = "{}[{}]".format(attr_name, self.datatype._index)
        return "{attr_name} {expression} list_append({attr_name}, {value_name})".format(
            attr_name=attr_name,
            expression=self.expression,
            value_name=self.expression_attribute_value_name)
