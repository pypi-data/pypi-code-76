class UpdateAction(object):
    """A class used specificallly for UpdateExpressionAttributes"""

    def __init__(self, action, expression):
        """constructor for UpdateAction

        Parameters:
            action: a string ADD | SET | DELETE | UPDATE
            expression: a BaseExpression
        """
        self.action = action
        self.expression = expression
