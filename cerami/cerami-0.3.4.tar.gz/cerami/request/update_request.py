from functools import singledispatch
from .mixins import BaseRequest, Keyable, Returnable
from ..response import SaveResponse
from ..datatype import DynamoDataType
from ..datatype.expression import (
    BaseExpression,
    UpdateRemoveExpression,
    EqualityExpression)
from .search_attribute import (
    DictAttribute,
    UpdateAction,
    UpdateExpressionAttribute)


class UpdateRequest(BaseRequest, Keyable, Returnable):
    """A class to perform the update request"""

    def execute(self):
        """perform the update_item request

        Returns:
        a SaveResponse object built from the update_item response

        For example::

            Person.update \\
                .key(Person.email == 'test@test.com') \\
                .set(Person.name, 'Mommy') \\
                .execute()
        """
        response = self.client.update_item(**self.build())
        return SaveResponse(response, self.reconstructor)

    def set(self, expression_or_datatype, value=None):
        """Add a SET statement to the UpdateExpression

        The UpdateExpression is a comma separated list of instructions to perform on the
        table. SET will change the value or put the value if it does not exist.

        Sorry, i dont know how to do method overloading in python yet, so were stuck with
        this garbage..

        Parameters:
            datatype_or_expresion: a DynamoDataType or BaseExpresion object to change
            value: the value to change the datatype

        Returns:
            the caller of the method. This allows for chaining

        For example::

            Person.update \\
                .key(Person.email == "test@test.com") \\
                .set(Person.name, "Zac") \\
                .execute()

            Person.update \\
                .key(Person.email == "test@test.com") \\
                .set(Person.age.add(10))
                .execute()
        """
        if isinstance(expression_or_datatype, BaseExpression):
            return self.update_expression('SET', expression_or_datatype)
        self.update_expression(
            'SET',
            EqualityExpression('=', expression_or_datatype, value),
        )
        return self

    def remove(self, *datatypes):
        """Add a REMOVE statement to the UpdateExpression

        The UpdateExpression is a comma separated list of instructions to perform on the
        table. REMOVE will delete the specified datatypes from the record. REMOVE can also
        be used to remove elements from a List datatype when used with List.index()

        Parameters:
            *datatypes: a list of DynamoDataType objects

        Returns:
            the caller of the method. This allows for chaining

        For example::

            Person.update \\
                .key(Person.email == "test@test.com") \\
                .remove(Person.name) \\
                .build()
            {
                "TableName": "people",
                "ReturnValues": "ALL_NEW",
                "Key": {
                    "email": {
                        "S": "test@test.com"
                    }
                },
                "UpdateExpression": "REMOVE #__name  :_name_butcw",
                "ExpressionAttributeNames": {
                    "#__name": "name"
                }
            }
        """
        for datatype in datatypes:
            expression = UpdateRemoveExpression(datatype)
            self.update_expression('REMOVE', expression)
        return self

    def add(self, datatype, value):
        """Add an ADD statement to the UpdateExpression

        **Amazon recommends only using with numbers and sets**

        The UpdateExpression is a comma separated list of instructions to perform on the
        table. ADD can be used to change the value of the Number or add to a Set.

        Parameters:
            datatype: a DynamoDataType object to change
            value: the value to change the datatype
                For Numbers the value should be a number, it can be negative to subtract
                For Sets, the value should be an array

        Returns:
            the caller of the method. This allows for chaining

        For example::

            Person.update.key(Person.email == "test@test.com").add(Person.age, 10).build()
            {
                "TableName": "people",
                "ReturnValues": "ALL_NEW",
                "Key": {
                    "email": {
                        "S": "test@test.com"
                    }
                },
                "UpdateExpression": "ADD #__age  :_age_dzszf",
                "ExpressionAttributeNames": {
                    "#__age": "age"
                },
                "ExpressionAttributeValues": {
                    ":_age_dzszf": {
                        "N": "10"
                    }
                }
            }
        """
        expression = EqualityExpression('', datatype, value)
        return self.update_expression('ADD', expression)

    def delete(self, datatype, value):
        """Add a DELETE statement to the UpdateExpression


        The UpdateExpression is a comma separated list of instructions to perform on the
        table. DELETE can be used to remove one or more elements from a Set only.

        Parameters:
            datatype: a Set DynamoDatatype object
            value: an array of values to remove from the set.

        Returns:
            the caller of the method. This allows for chaining

        For example::

            Person.update \\
                .key(Person.email == "test@test.com") \\
                .delete(Person.tags, ["cool", "awesome"]) \\
                .build()
            {
                "TableName": "people",
                "ReturnValues": "ALL_NEW",
                "Key": {
                    "name": {
                        "S": "test@test.com"
                    }
                },
                "UpdateExpression": "DELETE #__tags  :_tags_bttwj",
                "ExpressionAttributeNames": {
                    "#__tags": "tags"
                },
                "ExpressionAttributeValues": {
                    ":_tags_bttwj": {
                        "SS": [
                            "cool",
                            "awesome"
                        ]
                    }
                }
            }
        """
        expression = EqualityExpression('', datatype, value)
        return self.update_expression('DELETE', expression)

    def update_expression(self, action, expression):
        """return a Request setup with the update expression attributes

        Adds the UpdateExpression, ExpressionAttributeNames and ExpressionAttributeValues
        to the request_attributes dict

        Parameters:
            action: ADD | SET | DELETE | UPDATE
            expression: a BaseExpression object

        Returns:
            the caller of the method. This allows for chaining
        """
        name = {}
        name[expression.expression_attribute_name] = expression.datatype.column_name
        self.add_attribute(UpdateExpressionAttribute,
                           'UpdateExpression',
                           UpdateAction(action, expression))
        self.add_attribute(DictAttribute,
                           'ExpressionAttributeNames',
                           name)
        self.add_attribute(DictAttribute,
                           'ExpressionAttributeValues',
                           expression.value_dict())
        return self
