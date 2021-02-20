from ..response import SearchResponse
from .mixins import BaseRequest, Filterable, Projectable, Limitable, Pageable

class ScanRequest(BaseRequest, Filterable, Projectable, Limitable, Pageable):
    """A class to perform the scan request"""

    def execute(self):
        """perform the scan request

        Returns:
            a SearchResponse built from the scan response

        For example::

            Person.scan.filter(Person.name == "Mom").execute()
        """
        response = self.client.scan(**self.build())
        return SearchResponse(response, self.reconstructor)
