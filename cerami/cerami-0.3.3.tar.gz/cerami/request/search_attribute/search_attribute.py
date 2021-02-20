class SearchAttribute(object):
    """The base class for all attributes used for ``BaseRequest.add_attribute()``

    All Request objects have a ``request_attributes`` dict whose keys represent options
    for the request and values are different children of this base class.
    ``Request.build()`` iterates all of these attributes and calls this
    class' build method.

    All Request methods return a reference to the caller, so it is possible to chain
    multiple methods of the same thing together.  For example:: 

        Model.filter(Model.column1 == 1).filter(Model.column2 == 2)

    The search attribute needs to decide how to handle duplicate calls. It may want
    to overwrite the first value, or do something to append them, That logic is
    handled by ``SearchAttribute.add()``

    Attributes:
        value: Anything. It will be up to the ``build()`` method how to convert this value
            into a format suitable for DynamoDb
    """

    def __init__(self, value=None):
        """constructor for the SearchAttribute

        Parameters:
            value: it can by anything - whatever should be associated with the name
        """
        self.value = value

    def add(self, value):
        """setter for value

        All Request methods return a reference to the caller, so it is possible to chain
        multiple methods of the same thing together.
        For example, Model.filter(Model.column1 == 1).filter(Model.column2 == 2)

        The search attribute needs to decide how to handle duplicate calls. It may want
        to overwrite the first value, or do something to append them, That logic is
        handled by SearchAttribute.add()

        Parameters:
            value: A new value to be manipulated by the class
        """
        self.value = value

    def build(self):
        """build the SearchAttribute, which is called

        Request has a request_attributes dict whose keys represent options for the request
        and values are different children of this base class. Request.build() iterates all
        of these attributes and calls this SearchAttribute.build().

        Returns:
            the value
        """
        return self.value
