from mock import Mock, patch, call
from tests.helpers.testbase import TestBase
from cerami.response import SaveResponse
from cerami.request import PutRequest
from cerami.request.search_attribute import DictAttribute

class TestPutRequest(TestBase):
    def setUp(self):
        self.mocked_client = Mock()
        self.request  = PutRequest(
            tablename="test",
            client=self.mocked_client)

    def test_execute(self):
        """it calls put_item with the build
        it returns a SaveResponse
        """
        self.request.build = Mock()
        expected = {"fake": True}
        self.mocked_client.put_item.return_value = {'Test': True}
        self.request.build.return_value = expected
        res = self.request.execute()
        self.mocked_client.put_item.assert_called_with(fake=True)
        assert isinstance(res, SaveResponse)

    def test_item(self):
        """it calls adds the Item attribute with the item_dict"""
        self.request.add_attribute = Mock()
        fake_data = {}
        self.request.item(fake_data)
        calls = [call(DictAttribute, 'Item', fake_data)]
        self.request.add_attribute.assert_has_calls(calls)
