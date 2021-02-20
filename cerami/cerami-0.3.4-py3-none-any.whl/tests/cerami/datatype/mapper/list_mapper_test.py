from mock import Mock
from tests.helpers.testbase import TestBase
from cerami.datatype import String, List
from cerami.datatype.mapper import (
    ListMapper)

class TestListMapper(TestBase):
    def setUp(self):
        self.mocked_map_guesser = Mock()
        self.mocked_parse_guesser = Mock()
        self.dt = List()
        self.mapper = ListMapper(
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
        mocked_dt.mapper.resolve.return_value = "mocked"
        self.mocked_map_guesser.guess.return_value = mocked_dt
        val = ['test']
        res = self.mapper.resolve(val)
        assert res == ['mocked']
        self.mocked_map_guesser.guess.assert_called_with(0, 'test')
        mocked_dt.mapper.resolve.assert_called_with('test')

    def test_map(self):
        """it uses the guesser to find the correct datatype
        and returns a dict with the mapped value
        """
        mocked_dt = Mock()
        mocked_dt.mapper.resolve.return_value = "mocked"
        self.mocked_map_guesser.guess.return_value = mocked_dt
        val = ['test']
        res = self.mapper.map(val)
        assert res == {'L': ['mocked']}
        self.mocked_map_guesser.guess.assert_called_with(0, 'test')
        mocked_dt.mapper.resolve.assert_called_with('test')

    def test_parse(self):
        """it uses guesser to find the correct datatype
        based on the value and calls reconstruct for that datatype
        """
        mocked_dt = Mock()
        mocked_dt.mapper.reconstruct.return_value = "mocked"
        self.mocked_parse_guesser.guess.return_value = mocked_dt
        value = [{'S': 'testval'}]
        assert self.mapper.parse(value) == ['mocked']
        self.mocked_parse_guesser.guess.assert_called_with(
            0,
            {'S': 'testval'})
        mocked_dt.mapper.reconstruct.assert_called_with({'S': 'testval'})
