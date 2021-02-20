from mock import Mock
from tests.helpers.testbase import TestBase
from cerami.datatype.mapper import UniformListMapper


class TestUniformListMapper(TestBase):
    def setUp(self):
        self.mocked_mapper = Mock()
        self.mapper = UniformListMapper(self.mocked_mapper)

    def test__init__(self):
        """it sets mapper"""
        assert self.mapper.mapper == self.mocked_mapper

    def test_map(self):
        """it calls mocked_map for each item in the list and returns the dict"""
        self.mocked_mapper.map.return_value = 'mocked'
        val = [1]
        assert self.mapper.map(val) == {'L': ['mocked']}
        self.mocked_mapper.map.assert_called_with(1)

    def test_resolve(self):
        """it calls mocked_map for each value"""
        self.mocked_mapper.map.return_value = 'mocked'
        val = [1]
        assert self.mapper.resolve(val) == ['mocked']
        self.mocked_mapper.map.assert_called_with(1)

    def test_parse(self):
        """it calls mapper.reconstruct for each item in the list"""
        self.mocked_mapper.reconstruct.return_value = 'mocked'
        value = [{'S': 'test'}]
        assert self.mapper.parse(value) == ['mocked']
        self.mocked_mapper.reconstruct.assert_called_with({'S': 'test'})
