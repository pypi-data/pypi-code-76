from mock import Mock
from tests.helpers.testbase import TestBase
from cerami.response import SaveResponse

class TestSaveResponse(TestBase):
    def test__init__(self):
        """it calls reconstructor with the raw Attributes"""
        mocked_reconstructor = Mock()
        mocked_reconstructor.reconstruct.return_value = 'mocked'
        db_response = {'Attributes': {'test': True}}
        resp = SaveResponse(db_response, mocked_reconstructor)
        assert resp.item == 'mocked'
        mocked_reconstructor.reconstruct.assert_called_with(
            db_response['Attributes'])

    def test__init__keyerror(self):
        """it sets item to know when missing Attributes"""
        mocked_reconstructor = Mock()
        db_response = {}
        resp = SaveResponse(db_response, mocked_reconstructor)
        assert resp.item == None


