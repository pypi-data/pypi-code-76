from .base_expression import BaseExpression

class UpdateRemoveExpression(BaseExpression):
    """A class use specifically for ``UpdateRequest.remove()``

    A remove expression does not require  any values since it just needs the column_name.
    There isnt an example worth providing for this class. Remove expressions should really
    only be invoked through ``UpdateRequest.remove()``
    """

    def __init__(self, datatype):
        """Constructor for UpdateRemoveExpression

        Parameters:
            datatype: a DynamoDataType that should be removed from a record
        """
        super(UpdateRemoveExpression, self).__init__('', datatype, None)

    def value_dict(self):
        """there is no value for this expression so return an empty dict

        Normally, the ``value_dict()`` of an expression will return dictionary
        mapping the unique name to the value formatted for DynamoDB. However,
        an UpdateRemoveExpression has no values, which is why this returns an
        empty dict. Because ``UpdateRequest.update_expression()`` automatically
        tries to add the values for any expression, it is important this returns
        an empty dict so it does not break DynamoDB when submitting the request

        Returns:
            an empty dict
        """
        return {}
