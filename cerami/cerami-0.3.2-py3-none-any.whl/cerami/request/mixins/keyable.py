from ..search_attribute import DictAttribute

class Keyable(object):
    """A mixin to add the key method"""

    def key(self, *expressions):
        """return a new Request setup with the Key attribute

        Adds the Key to the request_attributes dict

        Args:
            *expressions: a list of ``BaseExpressions``

        Returns:
            the caller of the method. This allows for chaning

        For example::
        
            Person.get.key(Person.email == 'test@test.com').build()
            {
                "TableName": "people",
                "Key": {
                    "email": {
                        "S": "test@test.com"
                    }
                }
            }
        """
        for expression in expressions:
            key_dict = {}
            key_dict[expression.datatype.column_name] = expression.attribute_map()
            self.add_attribute(DictAttribute, 'Key', key_dict)
        return self
