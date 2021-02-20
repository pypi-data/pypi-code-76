from tests.helpers.testbase import TestBase
from cerami.datatype import Boolean
from cerami.datatype.mapper import BooleanMapper

class TestBooleanMapper(TestBase):
    def setUp(self):
        self.dt = Boolean()
        self.mapper = BooleanMapper(self.dt)

    def test_resolve(self):
        """it returns 1 for True 0 for False"""
        assert self.mapper.resolve(True) == True
        assert self.mapper.resolve(False) == False

    def test_parse(self):
        """it returns True for truthy values False for falsey values"""
        assert self.mapper.parse(True)
        assert not self.mapper.parse(False)

