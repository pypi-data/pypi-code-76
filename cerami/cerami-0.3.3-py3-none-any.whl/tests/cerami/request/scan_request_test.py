from mock import Mock, patch
from tests.helpers.testbase import TestBase
from cerami.response import SearchResponse
from cerami.request import ScanRequest
from cerami.request.mixins import Filterable, Projectable, Limitable, Pageable

class TestScanRequest(TestBase):
    def setUp(self):
        self.mocked_client = Mock()
        self.request = ScanRequest(
            tablename="test",
            client=self.mocked_client)

    def test_is_filterable(self):
        assert isinstance(self.request, Filterable)

    def test_is_limitable(self):
        assert isinstance(self.request, Limitable)

    def test_is_projectable(self):
        assert isinstance(self.request, Projectable)

    def test_is_pageable(self):
        assert isinstance(self.request, Pageable)

    def test_execute(self):
        """it calls scan with the build
        it returns a SearchResponse"""
        with patch("cerami.request.mixins.BaseRequest.build") as build:
            expected = {"fake": True}
            self.mocked_client.scan.return_value = {
                'Count': 0,
                'ScannedCount': 0}
            build.return_value = expected
            res = self.request.execute()
            self.mocked_client.scan.assert_called_with(fake=True)
            assert isinstance(res, SearchResponse)
