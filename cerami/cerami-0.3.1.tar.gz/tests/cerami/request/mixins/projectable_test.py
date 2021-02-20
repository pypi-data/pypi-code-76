from mock import patch, call, Mock, MagicMock
from tests.helpers.testbase import TestBase
from cerami.model import Model
from cerami.datatype import String
from cerami.request.search_attribute import (
    DictAttribute,
    ProjectionExpressionAttribute)
from cerami.request.mixins import Projectable

class TestModel(Model):
    test = String()

class TestRequest(Projectable):
    pass

class TestProjectable(TestBase):
    def setUp(self):
        self.request = TestRequest()

    @patch('cerami.request.mixins.projectable.BaseExpression')
    def test_project(self, expression_mock):
        """it adds FilterExpression, ExpresionAttributeNames,
        ExpressionAttributeValues"""
        expression_instance = MagicMock()
        expression_instance.expression_attribute_name = 'fake_name'
        expression_mock.return_value = expression_instance

        self.request.add_attribute = Mock()
        names = {'fake_name': 'test'}

        self.request.project(TestModel.test)
        calls = [
            call(ProjectionExpressionAttribute,
                 'ProjectionExpression',
                 expression_instance),
            call(DictAttribute,
                 'ExpressionAttributeNames',
                 names),
        ]
        self.request.add_attribute.assert_has_calls(calls)
