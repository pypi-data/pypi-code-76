class Response(object):
    """A BaseClass to handle the response from a Request

    All Request.execute() calls make a request to DynamoDB which returns the records
    and extra meta data about the request. A Response object is responsible for
    interpreting this data

    Attributes:
        reconstructor: a Reconstructor object to help interpret data
        _raw: The entire response objected returned from DynamoDB
    """
    def __init__(self, response, reconstructor):
        """constructor for a Response

        Parameters:
            response: a dict returned from DynamoDB based on a Request.execute() call
            reconstructor: a Reconstructor object to help interpret data
        """
        self._raw = response
        self.reconstructor = reconstructor
