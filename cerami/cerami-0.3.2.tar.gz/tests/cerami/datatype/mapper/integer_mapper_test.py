from tests.helpers.testbase import TestBase
from cerami.datatype import Number
from cerami.datatype.mapper import IntegerMapper

class TestIntegerMapper(TestBase):
    def setUp(self):
        self.dt = Number()
        self.mapper = IntegerMapper(self.dt)

    def test_resolve(self):
        """it returns the value as a string"""
        assert self.mapper.resolve(1) == '1'

    def test_parse(self):
        """it returns the value as an int"""
        assert self.mapper.parse('1') == 1
