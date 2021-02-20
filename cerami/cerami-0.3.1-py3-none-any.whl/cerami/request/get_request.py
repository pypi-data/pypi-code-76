from .mixins import BaseRequest, Keyable, Projectable
from ..response import GetResponse

class GetRequest(BaseRequest, Keyable, Projectable):
    """A class to perform the get_item request"""

    def execute(self):
        """perform the get_item request

        Returns:
            a GetResponse object built from the get_item response

        For example::

            Person.get.key(Person.email == 'test@test.com').execute()
        """
        response = self.client.get_item(**self.build())
        return GetResponse(response, self.reconstructor)

