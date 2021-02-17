# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.store_info import StoreInfo  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCommandApisController(BaseTestCase):
    """CommandApisController integration test stubs"""

    def test_summary_get(self):
        """Test case for summary_get

        Gives petstore's summary
        """
        response = self.client.open(
            '/v1/{basePath}/summary',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
