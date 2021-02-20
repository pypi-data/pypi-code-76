from mock import patch, call, Mock
from tests.helpers.testbase import TestBase
from cerami.model import Model
from cerami.datatype import String
from cerami.request.search_attribute import (
    DictAttribute,
    QueryExpressionAttribute)
from cerami.request.mixins import Filterable

class TestModel(Model):
    test = String()

class TestRequest(Filterable):
    pass

class TestFilterable(TestBase):
    def setUp(self):
        self.request = TestRequest()

    def test_filter(self):
        """it adds FilterExpression, ExpresionAttributeNames,
        ExpressionAttributeValues"""
        self.request.add_attribute = Mock()
        expression = TestModel.test == '123'
        names = {}
        names[expression.expression_attribute_name] = 'test'

        self.request.filter(expression)
        calls = [
            call(QueryExpressionAttribute,
                 'FilterExpression',
                 expression),
            call(DictAttribute,
                 'ExpressionAttributeNames',
                 names),
            call(DictAttribute,
                 'ExpressionAttributeValues',
                 expression.value_dict())
        ]
        self.request.add_attribute.assert_has_calls(calls)
