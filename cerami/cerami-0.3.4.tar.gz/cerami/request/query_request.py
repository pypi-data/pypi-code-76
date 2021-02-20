from .mixins import BaseRequest, Filterable, Keyable, Projectable, Limitable, Pageable
from ..response import SearchResponse
from .search_attribute import (
    SearchAttribute,
    DictAttribute,
    QueryExpressionAttribute)

class QueryRequest(BaseRequest, Filterable, Projectable, Limitable, Pageable):
    """ A class to perform the query request"""

    def execute(self):
        """perform the query request

        Returns:
            a SearchResponse built from the query response

        For example::

            Person.query.key(Person.email == "test@test.com").execute()
        """
        response = self.client.query(**self.build())
        return SearchResponse(response, self.reconstructor)

    def index(self, index_name, reverse=False):
        """add IndexName to the search_attributes

        Adds the IndexName to the request_attributes dict

        Parameters:
            index_name: a string of the index to query. It can be a local secondary
                index or global secondary index on the table
            reverse: a flag, that when true automatically sets `ScanIndexForward` to
                False.

        Returns:
            the instance of this class

        For example::

            Person.query.index("MyGlobalIndex).key(Person.name == 'Mom').build()
            {
                "TableName": "people",
                "IndexName": "MyGlobalIndex",
                "KeyConditionExpression": "#__name = :_name_lrhve",
                "ExpressionAttributeNames": {
                    "#__name": "name"
                },
                "ExpressionAttributeValues": {
                    ":_name_lrhve": {
                        "S": "Mom"
                    }
                }
            }
        """
        self.add_attribute(SearchAttribute, 'IndexName', index_name)
        if reverse:
            self.scan_index_forward(False)
        return self

    def scan_index_forward(self, value):
        """add the ScanIndexForward search_attribute

        It is used to reverse the sorting of the response

        Parameters:
            value: a boolean that specifies the ordering. Setting to `False` will reverse
                the order

        Returns:
            the instance of this class

        For example::

            Person.query.key(Person.name == 'Mom').scan_index_forward(False).build()
            {
                "TableName": "people",
                "KeyConditionExpression": "#__name = :_name_lrhve",
                "ExpressionAttributeNames": {
                    "#__name": "name"
                },
                "ScanIndexForward": False,
                "ExpressionAttributeValues": {
                    ":_name_lrhve": {
                        "S": "Mom"
                    }
                }
            }
        """
        self.add_attribute(SearchAttribute, 'ScanIndexForward', value)
        return self

    def key(self, *expressions):
        """return a new SearchInterface setup with query attributes

        The QueryRequest does not extend Keyable because it uses
        a different name for the attribute - KeyConditionExpression

        Parameters:
            *expressions: a list of BaseExpressions

        Returns:
            the instance of this class
        """
        for expression in expressions:
            names = {}
            names[expression.expression_attribute_name] = expression.datatype.column_name
            self.add_attribute(
                QueryExpressionAttribute,
                'KeyConditionExpression',
                expression)
            self.add_attribute(
                DictAttribute,
                'ExpressionAttributeNames',
                names)
            self.add_attribute(
                DictAttribute,
                'ExpressionAttributeValues',
                expression.value_dict())
        return self
