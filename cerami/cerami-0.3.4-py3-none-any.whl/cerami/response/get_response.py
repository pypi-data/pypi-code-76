from .response import Response

class GetResponse(Response):
    """A Response class to handle GetRequest

    Attributes:
        item: The reconstructed data from the response Item It will be None if the response
            for some reason is missing the ``Item`` key.
    """

    def __init__(self, response, reconstructor):
        """constructor for GetResponse

        Parameters:
            response: a dict from DynamoDB typically from a get_item request
            reconstructor: a Reconstructor object to help interpret data
        """
        super(GetResponse, self).__init__(response, reconstructor)
        try:
            self.item = self.reconstructor.reconstruct(self._raw['Item'])
        except KeyError:
            self.item = None
