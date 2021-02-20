from mock import patch, call, Mock
from tests.helpers.testbase import TestBase
from cerami.model import Model
from cerami.datatype import String
from cerami.request.search_attribute import SearchAttribute
from cerami.request.mixins import Returnable
from cerami.request.return_values import ALL_NEW

class TestModel(Model):
    test = String()

class TestRequest(Returnable):
    pass

class TestReturnable(TestBase):
    def setUp(self):
        self.request = TestRequest()

    def test_returns(self):
        """it adds ReturnValues"""
        self.request.add_attribute = Mock()
        self.request.returns(ALL_NEW)
        calls = [
            call(SearchAttribute, 'ReturnValues', ALL_NEW)
        ]
        self.request.add_attribute.assert_has_calls(calls)

