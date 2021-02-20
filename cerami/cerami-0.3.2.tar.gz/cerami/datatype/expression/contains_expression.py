from .base_expression import BaseExpression

class ContainsExpression(BaseExpression):
    """A class to generate a `CONTAINS` expression for querying/scanning

    `ContainsExpression` *cannot* be used in queries. It can only be used in filter
    expressions and condition expressions.

    For example::

        # You can use Person.email.contains instead!
        expression = ContainsExpression(Person.email, "test")
        Email.scan.filter(expression).build()
        {
            "TableName": "people",
            "FilterExpression": "contains(#__email, :_email_xfdww)",
            "ExpressionAttributeNames": {
                "#__email": "email"
            },
            "ExpressionAttributeValues": {
                ":_email_xfdww": {
                    "S": "test@test.com"
                }
            }
        }
    """
    def __init__(self, datatype, value):
        """constructor for BeginsWithExpression

        Parameters:
            datatype: a DynamoDataType that the expression is for
            value: check value to check if the datatype of an item contains
        """
        super(ContainsExpression, self).__init__('contains', datatype, value)

    def __str__(self):
        attr_name = self.expression_attribute_name
        if hasattr(self.datatype, '_index'):
            attr_name = "{}[{}]".format(attr_name, self.datatype._index)
        return "{expression}({attr_name}, {value})".format(
            attr_name=attr_name,
            expression=self.expression,
            value=self.expression_attribute_value_name)
