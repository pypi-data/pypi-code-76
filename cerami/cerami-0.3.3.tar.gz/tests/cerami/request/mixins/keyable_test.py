from mock import call, Mock
from tests.helpers.testbase import TestBase
from cerami.model import Model
from cerami.datatype import String
from cerami.request.search_attribute import DictAttribute
from cerami.request.mixins import Keyable

class TestModel(Model):
    test = String()

class TestRequest(Keyable):
    pass

class TestKeyable(TestBase):
    def setUp(self):
        self.request = TestRequest()

    def test_key(self):
        """it adds Key"""
        self.request.add_attribute = Mock()
        expression = TestModel.test == '123'
        key_dict = {}
        key_dict[expression.datatype.column_name] = expression.attribute_map()

        self.request.key(expression)
        calls = [
            call(DictAttribute, 'Key', key_dict)
        ]
        self.request.add_attribute.assert_has_calls(calls)
