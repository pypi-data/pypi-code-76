from mock import patch
from tests.helpers.testbase import TestBase
from cerami.datatype import String
from cerami.datatype.expression import InExpression
class TestInExpression(TestBase):
    def setUp(self):
        self.dt = String(column_name="testcol")

    def test__init__(self):
        with patch('cerami.datatype.expression.InExpression._build_expression_attribute_values') as build:
            build.return_value = 'mockedExpressionAttributeValues'
            expression = InExpression(self.dt, ['test'])
            assert expression.expression_attribute_values == 'mockedExpressionAttributeValues'

    def test_value_dict(self):
        """returns expression_attribute_values"""
        with patch('cerami.datatype.expression.InExpression._build_expression_attribute_values') as build:
            build.return_value = 'mockedExpressionAttributeValues'
            expression = InExpression(self.dt, ['test'])
            assert expression.value_dict() == 'mockedExpressionAttributeValues'


    def test__str__one_value(self):
        """it returns the expression without any commas in the values"""
        expression = InExpression(self.dt, ['test'])
        attr_name = expression.expression_attribute_name
        value_name = list(expression.value_dict().keys())[0]
        expected = "{} IN ({})".format(attr_name, value_name)
        assert str(expression) == expected

    def test__str__multiple_values(self):
        """it returns the expressions with comma separated values"""
        expression = InExpression(self.dt, ['test', 'test2'])
        attr_name = expression.expression_attribute_name
        value_names = list(expression.value_dict().keys())
        expected = "{} IN ({}, {})".format(attr_name, value_names[0], value_names[1])
        assert str(expression) == expected
