from ..search_attribute import DictAttribute

class Pageable(object):
    """A mixin to add the start_key method

    Pageable requests can be paginated by passing in an ExclusiveStartKey attribute.
    """

    def start_key(self, key):
        """return a new Request setup with the ExclusiveStartKey attribute

        Parameters:
            key: A dict representing the exclusive start key. This key is _excluded_
                from the response. Typically, this key is auto-generated from a previous
                response of a request.


        For example::

            request = Person.scan \\
                .limit(1) \\
                .start_key({"email": {"S": "test@test.com"}})

            request.build()
            {
                "TableName": "people",
                "Limit": 1,
                "ExclusiveStartKey": {
                    "email": {
                        "S": "test@test.com",
                    },
                },
            }

            # you can use the responses exclusive_start_key to continually paginate
            response = request.execute()
            next_response = request.start_key(response.last_evaludated_key).execute()
        """
        self.add_attribute(
            DictAttribute,
            'ExclusiveStartKey',
            key)
        return self
