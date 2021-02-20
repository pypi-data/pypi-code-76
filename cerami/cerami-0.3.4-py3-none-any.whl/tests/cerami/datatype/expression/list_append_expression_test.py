from mock import patch, Mock
from tests.helpers.testbase import TestBase
from cerami.datatype import List, String
from cerami.datatype.expression import ListAppendExpression

class TestListAppendExpression(TestBase):
    def setUp(self):
        self.dt = List(String(), column_name="testcol")
        with patch('cerami.datatype.expression.BaseExpression._generate_variable_name') as gen:
            gen.return_value = "mocked"
            self.expression = ListAppendExpression(self.dt, [1,2,3])

    def test__str__(self):
        """it returns list append structured expression"""
        expected = "#__testcol = list_append(#__testcol, mocked)"
        assert self.expression.__str__() == expected
