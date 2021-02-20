from .search_attribute import SearchAttribute

class QueryExpressionAttribute(SearchAttribute):
    """A class specifically to be used for QueryRequest.key()"""

    def __init__(self, value=None):
        """constructor for the Search Attribute

        Parameters:
            value: it should be an array of BaseExpressions
        """
        value = value or []
        super(QueryExpressionAttribute, self).__init__(value)

    def add(self, expression):
        """Update self.value by appending the new expression

        Arguments:
            expression: a BaseExpression
        """
        self.value.append(expression)

    def build(self):
        """Build a list of expressions separated by and

        KeyConditionExpression is a string of all different expressions that
        identify the keys of the table. It is the primary keys under most
        situation or can be whatever datatypes identify the index used for the query.
        """
        return ' and '.join(str(expr) for expr in self.value)
