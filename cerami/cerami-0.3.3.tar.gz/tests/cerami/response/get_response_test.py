from mock import Mock
from tests.helpers.testbase import TestBase
from cerami.response import GetResponse

class TestGetResponse(TestBase):
    def test__init__(self):
        """it calls reconstruct on item when the key is present"""
        mocked_reconstructor = Mock()
        mocked_reconstructor.reconstruct.return_value = 'mocked'
        db_response = {'Item': {'test': True}}
        resp = GetResponse(db_response, mocked_reconstructor)
        assert resp.item == 'mocked'
        mocked_reconstructor.reconstruct.assert_called_with(db_response['Item'])

    def test__init__keyerror(self):
        """it sets item to None when it is missing from _raw"""
        mocked_reconstructor = Mock()
        db_response = {}
        resp = GetResponse(db_response, mocked_reconstructor)
        assert resp.item == None
