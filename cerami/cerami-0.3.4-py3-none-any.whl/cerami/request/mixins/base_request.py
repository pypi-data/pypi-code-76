from copy import copy
from ...reconstructor import RawReconstructor
from ..search_attribute import SearchAttribute

class BaseRequest(object):
    """The Base Class for all requests

    It provides the default constructor and methods for building
    requests.

    Attributes:
        client: A ``boto3.client('dynamodb')``
        request_attributes:a dict of SearchAttribute objects whose
            keys represent options that can be passed to client upon execution
            For example, it may include a FilterExpression key whose value is
            a SearchAttribute that resolves to a string of filters. This is typically
            None but can be used to manually build requests::

                Parent.scan.filter(Parent.name == 'Mom').project(Parent.name)
                # The search_attributes can be manually specified
                ScanRequest(client=client, tablename='parents', search_attributes={
                    'FilterExpression': SearchAttribute('name = Mom'),
                    'ProjectionExpression': SearchAttribute('name'),
                })

        reconstructor: a Reconstructor object
    """

    def __init__(self, client, tablename="", request_attributes=None, reconstructor=None):
        """constructor for base request


        Parameters:
            client: A ``boto3.client('dynamodb')``
            tablename: the name of the table to perform the request on
            request_attributes:a dict of SearchAttribute objects whose
                keys represent options that can be passed to client upon execution
                For example, it may include a FilterExpression key whose value is
                a SearchAttribute that resolves to a string of filters. This is typically
                None but can be used to manually build requests::

                    Parent.scan.filter(Parent.name == 'Mom').project(Parent.name)
                    # The search_attributes can be manually specified
                    ScanRequest(client=client, tablename='parents', search_attributes={
                        'FilterExpression': SearchAttribute('name = Mom'),
                        'ProjectionExpression': SearchAttribute('name'),
                    })

            reconstructor: a Reconstructor object
        """
        self.request_attributes = copy(request_attributes or {})
        self.client = client
        self.reconstructor = reconstructor or RawReconstructor()
        if tablename:
            self.add_attribute(SearchAttribute, 'TableName', tablename)

    def __str__(self):
        return self.build().__str__()

    def add_attribute(self, attr_class, name, value):
        """add a search attribute to a to the request_attributes dict
        
        All search attributes must be unique keys. When the key already exists, it will
        update that value by calling ``add()``. Depending on the ``attr_class``, this
        can overwrite, append, change the value of the existing search attribute.

        Args:
            attr_class: a SearchAttribute class
            name: the name of the attribute
            value: the value that will be added to the SearchAttribute

        For example::

            Person.scan.limit(10)
            # or ...
            Person.scan.add_attribute(SearchAttribute, 'Limit', 10)
        """
        request_attribute = self.request_attributes.get(name, attr_class())
        request_attribute.add(value)
        self.request_attributes[name] = request_attribute
        return self

    def build(self):
        """build the dict used by dynamodb

        Returns:
            a dict whose keys matching the keys of the request_attributes and whose values
            are string versions of each attribute

        For example::

            User.scan.filter(User.email == 'test@test.com').build()
            {
                "TableName": "Users",
                "FilterExpression": "#__email = :_email_dpxqm",
                "ExpressionAttributeNames": {
                    "#__email": "email"
                },
                "ExpressionAttributeValues": {
                    ":_email_dpxqm": {
                        "S": "test@test.com"
                    }
                }
            }
        """
        return dict((k, v.build()) for k, v in self.request_attributes.items())
