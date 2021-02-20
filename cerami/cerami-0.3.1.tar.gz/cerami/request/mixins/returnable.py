from ..search_attribute import SearchAttribute

class Returnable(object):
    """A mixin to add the returns method"""

    def returns(self, value):
        """return the Request setup with ReturnValues attribute

        Adds the ReturnValues to the request attributes dict

        Args:
            value: NONE | ALL_OLD | UPDATED_OLD | ALL_NEW | UPDATED_NEW

        Returns:
            the caller of the method. This allows for chaining

        For example::


            from cerami.request.return_values import UPDATED_NEW
            Person.update \\
                .key(Person.email == 'test@test.com') \\
                .set(Person.name, 'new name') \\
                .returns(UPDATED_NEW) \\
                .build()
            {
                "TableName": "people",
                "ReturnValues": "UPDATED_NEW",
                "Key": {
                    "email": {
                        "S": "test@test.com"
                    }
                },
                "UpdateExpression": "SET #__name = :_name_zhvzz",
                "ExpressionAttributeNames": {
                    "#__name": "name"
                },
                "ExpressionAttributeValues": {
                    ":_name_zhvzz": {
                        "S": "new name"
                    }
                }
            }
        """
        self.add_attribute(
            SearchAttribute,
            'ReturnValues',
            value)
        return self
