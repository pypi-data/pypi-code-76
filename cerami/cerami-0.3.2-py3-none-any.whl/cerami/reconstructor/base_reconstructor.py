class BaseReconstructor(object):
    """The base class for all Reconstructors

    Reconstructors are used to interpret data from a DynamoDB response. All
    classes that inherit from BaseReconstructor implement ``reconstruct()`` which
    takes in the DynamoDB data and manipulates it accordingly.

    For example, the ModelReconstructor converts the raw DynamoDB response data back
    into the Model of the corresponding table
    """

    def reconstruct(self, item_dict):
        """The abstract reconstruct method to be implemented by child classes

        Its purpose it to convert the item_dict from DynamoDB

        Parameters:
            item_dict: a dict from DynamoDB. It will be in the format like
                ``{"a_column": {"S": "my_value"}}``

        Raises:
            Exception: Not Implemented
        """
        raise Exception("Not implemented")
