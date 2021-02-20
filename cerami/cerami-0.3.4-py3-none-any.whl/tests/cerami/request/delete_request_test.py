from mock import Mock, patch, call
from tests.helpers.testbase import TestBase
from cerami.response import DeleteResponse
from cerami.request import DeleteRequest
from cerami.request.mixins import Returnable, Keyable

class TestDeleteRequest(TestBase):
    def setUp(self):
        self.mocked_client = Mock()
        self.request  = DeleteRequest(
            tablename="test",
            client=self.mocked_client)

    def test_is_returnable(self):
        """it is returnable"""
        assert isinstance(self.request, Returnable)

    def test_is_keyable(self):
        """it is keyable"""
        assert isinstance(self.request, Keyable)

    def test_execute(self):
        """it calls delete_item with the build
        it returns a DeleteResponse
        """
        self.request.build = Mock()
        expected = {"fake": True}
        self.mocked_client.delete_item.return_value = {'Test': True}
        self.request.build.return_value = expected
        res = self.request.execute()
        self.mocked_client.delete_item.assert_called_with(fake=True)
        assert isinstance(res, DeleteResponse)

