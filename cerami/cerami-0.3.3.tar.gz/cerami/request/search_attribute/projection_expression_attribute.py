from .search_attribute import SearchAttribute

class ProjectionExpressionAttribute(SearchAttribute):
    """A class specifically to be used with the Projectable mixin"""

    def __init__(self, value=None):
        """constructor for the SearchAttribute

        Parameters:
            value: it should be an array of BaseExpressions.
        """
        value = value or []
        super(ProjectionExpressionAttribute, self).__init__(value)

    def add(self, expression):
        """Update self.value by appending the new expression

        Parameters:
            expression: a BaseExpression
        """
        self.value.append(expression)

    def build(self):
        """Build a comma separated list of all expressions in value

        ProjectionExpression is a comma separated list of all datatypes that should be 
        returned by  the request. All expressions in the value array are just
        empty expressions containing the Datatype.column_name

        Returns:
            A string of all expressions separated by commas
        """
        return ', '.join(str(expr) for expr in self.value)
