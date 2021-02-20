from ..search_attribute import (
    DictAttribute,
    QueryExpressionAttribute)

class Filterable(object):
    """A mixin to add the filter method"""

    def filter(self, *expressions):
        """return a new Request setup with filter attributes

        Adds the FilterExpression, ExpressionAttributeNames, and
        ExpressionAttributeValue to the request_attributes dict

        Args:
            *expressions: a list of ``BaseExpressions``

        Returns:
            the caller of the method. This allows for chaining

        For example::

            Person.scan.filter(Person.name == 'Zac').filter(Person.age < 50).build()
            {
                "TableName": "people",
                "FilterExpression": "#__name = :_name_pwmbx and #__age < :_age_twtue",
                "ExpressionAttributeNames": {
                    "#__name": "name",
                    "#__age": "age"
                },
                "ExpressionAttributeValues": {
                    ":_name_pwmbx": {
                        "S": "Zac"
                    },
                    ":_age_twtue": {
                        "N": "50"
                    }
                }
            }
        """
        for expression in expressions:
            names = {}
            names[expression.expression_attribute_name] = expression.datatype.column_name
            self.add_attribute(
                QueryExpressionAttribute,
                'FilterExpression',
                expression)
            self.add_attribute(
                DictAttribute,
                'ExpressionAttributeNames',
                names)
            self.add_attribute(
                DictAttribute,
                'ExpressionAttributeValues',
                expression.value_dict())
        return self
