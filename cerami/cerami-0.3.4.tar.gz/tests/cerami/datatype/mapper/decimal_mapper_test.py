from tests.helpers.testbase import TestBase
from cerami.datatype import Number
from cerami.datatype.mapper import DecimalMapper
from decimal import Decimal

class TestDecimalMapper(TestBase):
    def setUp(self):
        self.dt = Number()
        self.mapper = DecimalMapper(self.dt)

    def test_resolve(self):
        """it returns the value as a string"""
        assert self.mapper.resolve(1) == '1'
        assert self.mapper.resolve(123.456) == '123.456'

    def test_parse(self):
        """it returns the value as a decimal"""
        assert self.mapper.parse('1') == Decimal('1')
        assert self.mapper.parse('123.456') == Decimal('123.456')
