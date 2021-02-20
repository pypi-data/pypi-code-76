from mock import Mock, patch, call
from tests.helpers.testbase import TestBase
from cerami.response import GetResponse
from cerami.request import GetRequest
from cerami.request.mixins import Keyable, Projectable

class TestGetRequest(TestBase):
    def setUp(self):
        self.mocked_client = Mock()
        self.request  = GetRequest(
            tablename="test",
            client=self.mocked_client)

    def test_is_keyable(self):
        """it is keyable"""
        assert isinstance(self.request, Keyable)

    def test_is_projectable(self):
        assert isinstance(self.request, Projectable)

    def test_execute(self):
        """it calls get_item with the build
        it returns a GetResponse
        """
        self.request.build = Mock()
        expected = {"fake": True}
        self.mocked_client.get_item.return_value = {'Test': True}
        self.request.build.return_value = expected
        res = self.request.execute()
        self.mocked_client.get_item.assert_called_with(fake=True)
        assert isinstance(res, GetResponse)


