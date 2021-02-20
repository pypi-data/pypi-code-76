from tests.helpers.testbase import TestBase
from cerami.datatype import String
from cerami.datatype.mapper import StringMapper

class TestStringMapper(TestBase):
    def setUp(self):
        self.dt = String()
        self.mapper = StringMapper(self.dt)

    def test_resolve(self):
        """it returns the value as a string"""
        assert self.mapper.resolve(1) == "1"
