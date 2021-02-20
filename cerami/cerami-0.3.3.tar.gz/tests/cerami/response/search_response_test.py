from mock import Mock
from tests.helpers.testbase import TestBase
from cerami.response import SearchResponse

class TestSearchResponse(TestBase):
    def setUp(self):
        self.mocked_reconstructor = Mock()
        self.db_response = {
            'Count': 1,
            'ScannedCount': 1,
            'LastEvaluatedKey': 'test',
            'Items': [{'fake': True}]}
        self.resp = SearchResponse(
            self.db_response,
            self.mocked_reconstructor)

    def test__init__(self):
        assert self.resp.count == 1
        assert self.resp.scanned_count == 1
        assert self.resp.last_evaluated_key == 'test'
        assert self.resp._items == [{'fake': True}]

    def test_items(self):
        """it returns an iterable list of reconstructoed items"""
        self.mocked_reconstructor.reconstruct.return_value = 'mocked'
        items = iter(self.resp.items)
        assert next(items) == 'mocked'
        self.mocked_reconstructor.reconstruct.assert_called_with({'fake': True})
        

    def test__init__keyerror(self):
        """it sets items to [] when it is missing"""
        del self.db_response['Items']
        resp = SearchResponse(self.db_response, self.mocked_reconstructor)
        assert resp._items == []
