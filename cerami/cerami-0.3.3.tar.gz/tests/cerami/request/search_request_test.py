from mock import patch, call, Mock
from tests.helpers.testbase import TestBase
import cerami.datatype as dt
from cerami.model import Model
from cerami.datatype import String
from cerami.datatype.expression import EqualityExpression
from cerami.request.search_attribute import (
    SearchAttribute,
    DictAttribute,
    QueryExpressionAttribute,)
from cerami.request import SearchRequest

class TestModel(Model):
    test = String()

class TestSearchRequest(TestBase):
    def setUp(self):
        self.client = Mock()
        self.request = SearchRequest(self.client, tablename='testtable')

    def test_add_attribute(self):
        """it calls add for the search attribute"""
        with patch("cerami.request.search_attribute.SearchAttribute.add") as add:
            self.request.add_attribute(SearchAttribute, 'Test', 123)
            assert isinstance(
                self.request.search_attributes['Test'],
                SearchAttribute)
            add.assert_called_with(123)

    def test_filter(self):
        """it adds FilterExpression, ExpresionAttributeNames,
        ExpressionAttributeValues"""
        with patch("cerami.request.SearchRequest.add_attribute") as add:
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
            add.assert_has_calls(calls)

    def test_build(self):
        """returns a dict for all search_attributes"""
        self.request.add_attribute(SearchAttribute, 'Test', 123)
        built = self.request.build()
        expected = {
            "TableName": "testtable",
            "Test": 123,
        }
        assert built == expected

    def test_return_values(self):
        """it calls add_attribute with the value"""
        self.request.add_attribute = Mock()
        self.request.return_values('test')
        self.request.add_attribute.assert_called_with(
            SearchAttribute,
            'ReturnValues',
            'test')
