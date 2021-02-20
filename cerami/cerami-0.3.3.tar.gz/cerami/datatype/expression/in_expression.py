from .base_expression import BaseExpression

class InExpression(BaseExpression):
    """A class to generate an `IN` expression for filtering

    For example::

        # You can use Person.name.in_ instead!
        expression = InExpression(Person.name, ["Mom", "Dad"])
        Person.scan.filter(expression).build()
        {
            "TableName": "people",
            "FilterExpression": "#__name IN (:_name_qmtxc, :_name_wzhlh)",
            "ExpressionAttributeNames": {
                "#__name": "name"
            },
            "ExpressionAttributeValues": {
                ":_name_qmtxc": {
                    "S": "Mom"
                },
                ":_name_wzhlh": {
                    "S": "Dad"
                }
            }
        }
    """
    def __init__(self, datatype, value):
        """constructor for InExpression

        Parameters:
            datatype: a DynamoDataType that the expression is for
            value: an array of values
        """
        super(InExpression, self).__init__('IN', datatype, value)
        self.expression_attribute_values = self._build_expression_attribute_values()

    def __str__(self):
        value_names = ', '.join([k for k,v in self.value_dict().items()])
        attr_name = self.expression_attribute_name
        if hasattr(self.datatype, '_index'):
            attr_name = "{}[{}]".format(attr_name, self.datatype._index)
        return "{attr_name} {expression} ({value_names})".format(
            attr_name=attr_name,
            expression=self.expression,
            value_names=value_names)

    def value_dict(self):
        """return the expected dict for expression-attribute-values

        This is used by many of different requests when building search_attributes. Most
        requests require the `ExpressionAttributeValue` option. This will build that
        corresponding property for this particular expression. Since the value
        is an array, this method overrides the ``BaseExpression`` implementation.

        Returns:
            a dict that can be used in ExpressionAttributeValue options
        """
        return self.expression_attribute_values

    def _build_expression_attribute_values(self):
        column_name_safe = self.datatype.column_name.replace('.', '_')
        res = {}
        for v in self.value:
            value_name = self._generate_variable_name(column_name_safe)
            value_mapped = self.datatype.mapper.map(v)
            res[value_name] = value_mapped
        return res
