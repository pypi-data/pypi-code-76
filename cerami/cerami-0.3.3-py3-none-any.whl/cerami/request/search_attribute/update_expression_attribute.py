from .search_attribute import SearchAttribute

class UpdateExpressionAttribute(SearchAttribute):
    """A SearchAttribute used exclusively for ``UpdateRequest``

    Its value is a dict, whose keys are one the update actions ADD | SET | DELETE | UPDATE
    The value of each corresponding key is an array of expressions. This is so each action
    is unique during the build process and the expressions are comma separated::

        Model.add(Model.a_number(10)).add(Model.other_number(20))
        # becomes
        "ADD a_number 10, other_number 20"
    """

    def __init__(self, value=None):
        """constructor for the SearchAttribute

        Parameters:
            value: it should be a dict whose keys are arrays of expressions
        """
        value = value or {}
        super(UpdateExpressionAttribute, self).__init__(value)

    def add(self, update_action):
        """Update the self.value with the update_action

        It will create the array automatically if the key is missing or will append it

        Parameters:
            update_action: an UpdateAction object
        """
        if self.value.get(update_action.action):
            self.value[update_action.action].append(update_action.expression)
        else:
            self.value[update_action.action] = [update_action.expression]

    def build(self):
        """return all grouped expressions of value

        iterate over all keys and create a comma separated string of all expressions for
        each corresponding value array.

        Returns:
            a string of all expressions
        """
        operations = []
        for action, expressions in self.value.items():
            operation = action + ' ' + ', '.join(str(expr) for expr in expressions)
            operations.append(operation)
        return ' '.join(o for o in operations)
