from .response import Response

class SearchResponse(Response):
    """A Response class to handle SearchRequest

    A SearchResponse is returned from a ScanRequest or QueryRequest

    Attributes:
        count: The number of records returned
        scanned_count: I dont really know how this one works yet
        last_evaluated_key: The primary key of the item where the operation stopped,
            inclusive of the result set. Can be used for pagination for the start value
            in the next query.
        _items: The raw data of all records in the result set
    """

    def __init__(self, response, reconstructor):
        """Constructor for SearchResponse

        Parameters:
            response: a dict from DynamoDB typically from a scan or query request
            reconstructor: a Reconstructor object to help interpret data
        """
        super(SearchResponse, self).__init__(response, reconstructor)
        self.count = self._raw['Count']
        self.scanned_count = self._raw['ScannedCount']
        self.last_evaluated_key = self._raw.get('LastEvaluatedKey')
        self._items = self._raw.get('Items', [])

    @property
    def items(self):
        """A generator to get individual items from the response

        Whenever an item is yielded, it will reconstruct the item using the reconstructor

        Returns:
            A generator to iterate over items in the response

        For example::

            response = Person.scan.filter(Person.age < 100).execute()
            for person in response.items:
                print(person.name)
        """
        for item in self._items:
            yield self.reconstructor.reconstruct(item)
