from .mixins import BaseRequest
from .search_attribute import DictAttribute
from ..response import SaveResponse

class PutRequest(BaseRequest):
    """A class to perform the put_item request"""

    def execute(self):
        """perform the put_item request

        Returns:
            a SaveResponse object built from the put_item response

        For example::

            Person.put.item({"email": {"S": "test@test.com"}}).execute()
        """
        response = self.client.put_item(**self.build())
        return SaveResponse(response, self.reconstructor)

    def item(self, item_dict):
        """add the item_dict to the search_attributes

        Adds the Item to the request_attributes dict

        Parameters:
            item_dict: a dict mapped to the DynamoDB format. Typically this is done
                through ``Model.as_item()``

        Returns:
            the caller of the method. This allows for chaining

        For example::

            person = Person(email="person@test.com")
            Person.put.item(person.as_item())
            Person.put.item({"email": {"S": "test@test.com"}).build()
            {
                "TableName": "people",
                "Item": {
                    "email": {
                        "S": "test@test.com"
                    }
                }
            }
        """
        self.add_attribute(DictAttribute, 'Item', item_dict)
        return self
