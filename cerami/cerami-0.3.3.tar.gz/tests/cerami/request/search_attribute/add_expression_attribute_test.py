from tests.helpers.testbase import TestBase
from cerami.dynamo_search_interface.search_attribute import AddExpressionAttribute
from cerami.model import Model
from cerami.datatype import Number
from cerami.datatype.expression import UpdateAddExpression

class FakeModel(Model):
    test = Number()

class TestAddExpressionAttribute(TestBase):
    def setUp(self):
        self.attribute = AddExpressionAttribute("Test")

    def test_add(self):
        """it adds the expression to the array"""
        expression = UpdateAddExpression(FakeModel.test, 10)
        self.attribute.add(expression)
        assert self.attribute.value == [expression]

    def test_build(self):
        """returns all expressions joined by ' and '"""
        expression = UpdateAddExpression(FakeModel.test, 10)
        self.attribute.add(expression)
        expected = "ADD {}".format(expression)
        assert self.attribute.build() == expected

