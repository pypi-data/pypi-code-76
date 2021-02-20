from .response import Response

class SaveResponse(Response):
    """A Response class to handle saves requests

    SaveResponses are generated through PutRequest and UpdateRequest
    """

    def __init__(self, response, reconstructor):
        """constructor for SaveResponse

        Parameters:
            response: a dict from DynamoDB typicall from put_item or update_item
            reconstructor: a Reconstructor object to help interpret data
        """
        super(SaveResponse, self).__init__(response, reconstructor)
        try:
            self.item = self.reconstructor.reconstruct(self._raw['Attributes'])
        except KeyError:
            self.item = None
