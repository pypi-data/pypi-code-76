from mock import patch, Mock
from tests.helpers.testbase import TestBase
from cerami.datatype import String
from cerami.datatype.expression import BaseExpression

class TestBaseExpression(TestBase):
    def setUp(self):
        self.dt = String(column_name="testcol")
        with patch('cerami.datatype.expression.BaseExpression._generate_variable_name') as gen:
            gen.return_value = "mocked"
            self.expression = BaseExpression('=', self.dt, 'test')

    def test__init__(self):
        assert self.expression.expression == '='
        assert self.expression.datatype == self.dt
        assert self.expression.value == 'test'
        assert self.expression.expression_attribute_name == '#__testcol'
        assert self.expression.expression_attribute_value_name == 'mocked'

    def test__str__(self):
        """it returns the expression equation"""
        assert self.expression.__str__() == "#__testcol = mocked"

    def test__str__index(self):
        """it includes the index in the string when _index is set on datatype"""
        self.expression.datatype._index = 1
        assert self.expression.__str__() == "#__testcol[1] = mocked"

    def test_attribute_map(self):
        """it calls the datatype mapper with the value"""
        self.expression.datatype = Mock()
        self.expression.attribute_map()
        self.expression.datatype.mapper.map.assert_called_with('test')

    def test_value_dict(self):
        """it returns the dict assigning the condition_type as the
        key to the value"""
        res = self.expression.value_dict()
        assert res == {"mocked": {"S": "test"}}
