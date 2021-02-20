from mock import patch, Mock
from tests.helpers.testbase import TestBase
from cerami.datatype import String
from cerami.datatype.mapper import BaseDatatypeMapper

class TestBaseDatatypeMapper(TestBase):
    def setUp(self):
        self.dt = String()
        self.mapper = BaseDatatypeMapper(self.dt)

    def test_map_none(self):
        """it returns the NULL object when value is None"""
        assert self.mapper.map(None) == {'NULL': True}

    def test_map(self):
        """it returns a dict
        with the key the condition_type
        and the value the result of resolve()
        """
        with patch('cerami.datatype.mapper.BaseDatatypeMapper.resolve') as resolve:
            resolve.return_value = "mocked"
            res = self.mapper.map('test')
            assert res == {"S": "mocked"}

    def test_reconstruct_null(self):
        """it returns None when mapped_dict is NULL"""
        assert self.mapper.reconstruct({'NULL': True}) == None

    def test_reconstruct_calls_parse(self):
        """calls parse when the value is not NULL"""
        self.mapper.parse = Mock()
        self.mapper.reconstruct({'S': 'test'})
        self.mapper.parse.assert_called_with('test')

    def test_parse(self):
        """parse returns the value"""
        assert self.mapper.parse('test') == 'test'
