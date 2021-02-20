from mock import Mock
from tests.helpers.testbase import TestBase
from cerami.response import Response

class TestResponse(TestBase):
    def test__init__(self):
        mocked_reconstructor = Mock()
        db_response = {'test': True}
        resp = Response(db_response, mocked_reconstructor)
        assert resp._raw == db_response
        assert resp.reconstructor == mocked_reconstructor
