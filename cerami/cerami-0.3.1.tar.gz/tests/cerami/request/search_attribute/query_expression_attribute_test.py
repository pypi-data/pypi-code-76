from tests.helpers.testbase import TestBase
from cerami.request.search_attribute import QueryExpressionAttribute
from cerami.model import Model
from cerami.datatype import String

class FakeModel(Model):
    test = String()
    test2 = String()

class TestQueryExpressionAttribute(TestBase):
    def setUp(self):
        self.attribute = QueryExpressionAttribute()

    def test_add(self):
        """it adds the expression to the array"""
        expression = FakeModel.test == '123'
        self.attribute.add(expression)
        assert self.attribute.value == [expression]

    def test_build(self):
        """returns all expressions joined by ' and '"""
        expr1 = FakeModel.test == '123'
        expr2 = FakeModel.test == '456'
        self.attribute.add(expr1)
        self.attribute.add(expr2)
        expected = "{} and {}".format(expr1, expr2)
        assert self.attribute.build() == expected
