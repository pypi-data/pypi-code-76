from .mixins import BaseRequest, Keyable, Returnable
from ..response import DeleteResponse

class DeleteRequest(BaseRequest, Keyable, Returnable):
    """A class to perform delete_item request"""

    def execute(self):
        """perform the delete_item request

        Returns:
            a DeleteResponse object built from the delete_item response

        For example::

            Person.delete.key(Person.email == 'test@test.com').execute()
        """
        response = self.client.delete_item(**self.build())
        return DeleteResponse(response, self.reconstructor)
