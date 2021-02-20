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
from cerami.request.mixins import BaseRequest

class TestModel(Model):
    test = String()

class TestBaseRequest(TestBase):
    def setUp(self):
        self.client = Mock()
        self.request = BaseRequest(self.client, tablename='testtable')

    def test_add_attribute(self):
        """it calls add for the search attribute"""
        with patch("cerami.request.search_attribute.SearchAttribute.add") as add:
            self.request.add_attribute(SearchAttribute, 'Test', 123)
            assert isinstance(
                self.request.request_attributes['Test'],
                SearchAttribute)
            add.assert_called_with(123)
