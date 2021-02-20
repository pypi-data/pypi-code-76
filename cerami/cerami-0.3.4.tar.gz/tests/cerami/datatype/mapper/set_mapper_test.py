from mock import patch, Mock, call
from tests.helpers.testbase import TestBase
from cerami.datatype import String
from cerami.datatype.mapper import (
    BaseDatatypeMapper,
    SetMapper)

class TestSetMapper(TestBase):
    def setUp(self):
        self.dt = String()
        self.mapper = BaseDatatypeMapper(self.dt)
        self.mapper.condition_type = 'S'
        self.decorator = SetMapper(self.mapper)

    def test__init__(self):
        assert self.decorator.mapper == self.mapper

    def test_map(self):
        with patch("cerami.datatype.mapper.SetMapper.resolve") as resolve:
            resolve.return_value = 'mocked'
            res = self.decorator.map(['test'])
            assert res == {"SS": "mocked"}

    def test_resolve(self):
        """it calls mapper.resolve for each item in value"""
        self.decorator.mapper = Mock()
        self.decorator.mapper.resolve.return_value = "mocked"
        calls = [call(1), call(2)]
        res = self.decorator.resolve([1,2])
        assert res == ['mocked', 'mocked']
        self.decorator.mapper.resolve.assert_has_calls(calls)

    def test_parse(self):
        """assigns the value directly from mapped_dict"""
        value = ['zac', 'test']
        assert self.decorator.parse(value) == ['zac', 'test']
