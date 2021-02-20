from mock import Mock
from tests.helpers.testbase import TestBase
from cerami.datatype import String, Map
from cerami.datatype.mapper import (
    DictMapper)

class TestDictMapper(TestBase):
    def setUp(self):
        self.mocked_map_guesser = Mock()
        self.mocked_parse_guesser = Mock()
        self.dt = Map()
        self.mapper = DictMapper(
            self.dt,
            self.mocked_map_guesser,
            self.mocked_parse_guesser)

    def test__init__(self):
        """it sets guesser"""
        assert self.mapper.map_guesser == self.mocked_map_guesser
        assert self.mapper.parse_guesser == self.mocked_parse_guesser

    def test_resolve(self):
        """it uses guesser to find the correct datatype
        based on the value and calls map for that datatype
        """
        mocked_dt = Mock()
        mocked_dt.mapper.map.return_value = "mocked"
        self.mocked_map_guesser.guess.return_value = mocked_dt
        val = {'test': 1}
        res = self.mapper.resolve(val)
        assert res == {'test': 'mocked'}
        self.mocked_map_guesser.guess.assert_called_with('test', 1)
        mocked_dt.mapper.map.assert_called_with(1)

    def test_parse(self):
        """it uses guesser to find the correct datatype
        based on the value and calls reconstruct for that datatype
        """
        mocked_dt = Mock()
        mocked_dt.mapper.reconstruct.return_value = "mocked"
        self.mocked_parse_guesser.guess.return_value = mocked_dt
        mapped_dict = {'M': {'testkey': {'S': 'testval'}}}
        assert self.mapper.reconstruct(mapped_dict) == {'testkey': 'mocked'}
        self.mocked_parse_guesser.guess.assert_called_with(
            'testkey',
            {'S': 'testval'})
        mocked_dt.mapper.reconstruct.assert_called_with({'S': 'testval'})
