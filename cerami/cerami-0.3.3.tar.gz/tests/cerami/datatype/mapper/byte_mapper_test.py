from tests.helpers.testbase import TestBase
from cerami.datatype import ByteBuffer
from cerami.datatype.mapper import ByteMapper

class TestByteMapper(TestBase):
    def setUp(self):
        self.dt = ByteBuffer()
        self.mapper = ByteMapper(self.dt)

    def test_resolve(self):
        """it returns the value as a string"""
        assert self.mapper.resolve('hello') == 'hello'.encode('utf-8')

    def test_parse(self):
        """it returns the value an encoded"""
        assert self.mapper.resolve('hello') == 'hello'.encode('utf-8')

