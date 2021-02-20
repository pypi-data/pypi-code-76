from .base_expression import BaseExpression

class BeginsWithExpression(BaseExpression):
    """A class to generate a `BEGINS WITH` expression for querying/scanning

    When using with a `QueryRequest`, a `BeginsWithExpression` can only be used on the
    sort key. It cannot be used on the partition key

    For example::

        # You can use Person.email.begins_with instead!
        expression = BeginsWithExpression(Person.email, "test")
        Email.scan.filter(expression).build()
        {
            "TableName": "people",
            "FilterExpression": "begins_with(#__email, :_email_xfdww)",
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
            value: a substring to check the column begins with
        """
        super(BeginsWithExpression, self).__init__('begins_with', datatype, value)

    def __str__(self):
        attr_name = self.expression_attribute_name
        if hasattr(self.datatype, '_index'):
            attr_name = "{}[{}]".format(attr_name, self.datatype._index)
        return "{expression}({attr_name}, {value})".format(
            attr_name=attr_name,
            expression=self.expression,
            value=self.expression_attribute_value_name)
