from mock import Mock, patch, call
from tests.helpers.testbase import TestBase
from cerami.model import Model
from cerami.datatype import String
from cerami.response import SearchResponse
from cerami.request import QueryRequest
from cerami.request.search_attribute import (
    SearchAttribute,
    DictAttribute,
    QueryExpressionAttribute)
from cerami.request.mixins import Filterable, Projectable, Limitable, Pageable

class TestModel(Model):
    test = String()

class TestQueryRequest(TestBase):
    def setUp(self):
        self.mocked_client = Mock()
        self.request  = QueryRequest(
            tablename="test",
            client=self.mocked_client)

    def test_is_filterable(self):
        """it is filterable"""
        assert isinstance(self.request, Filterable)

    def test_has_key_method(self):
        """it is keyable"""
        assert hasattr(self.request, 'key')

    def test_is_projectable(self):
        assert isinstance(self.request, Projectable)

    def test_is_limitable(self):
        assert isinstance(self.request, Limitable)

    def test_is_pageable(self):
        assert isinstance(self.request, Pageable)

    def test_index(self):
        """it adds the IndexName to the request"""
        self.request.add_attribute = Mock()
        self.request.index('test-index')
        self.request.add_attribute.assert_called_with(
            SearchAttribute,
            'IndexName',
            'test-index')

    def test_index_reverse(self):
        """it calls scan_index_forward(False) when reverse is true"""
        self.request.add_attribute = Mock()
        self.request.scan_index_forward = Mock()
        self.request.index('test-index', reverse=True)
        self.request.scan_index_forward.assert_called_with(False)
        self.request.add_attribute.assert_called_with(
            SearchAttribute,
            'IndexName',
            'test-index')

    def test_scan_index_forward(self):
        """it adds the ScanIndexForward attribute to the request"""
        self.request.add_attribute = Mock()
        self.request.scan_index_forward(False)
        self.request.add_attribute.assert_called_with(
            SearchAttribute,
            'ScanIndexForward',
            False)

    def test_execute(self):
        """it calls query with the build
        it returns a SearchResponse"""
        with patch("cerami.request.mixins.BaseRequest.build") as build:
            expected = {"fake": True}
            self.mocked_client.query.return_value = {
                'Count': 0,
                'ScannedCount': 0}
            build.return_value = expected
            res = self.request.execute()
            self.mocked_client.query.assert_called_with(fake=True)
            assert isinstance(res, SearchResponse)

    def test_key(self):
        self.request.add_attribute = Mock()
        expression = TestModel.test == '123'
        names = {}
        names[expression.expression_attribute_name] = 'test'

        self.request.key(expression)
        calls = [
            call(QueryExpressionAttribute,
                 'KeyConditionExpression',
                 expression),
            call(DictAttribute,
                 'ExpressionAttributeNames',
                 names),
            call(DictAttribute,
                 'ExpressionAttributeValues',
                 expression.value_dict())
        ]
        self.request.add_attribute.assert_has_calls(calls)
