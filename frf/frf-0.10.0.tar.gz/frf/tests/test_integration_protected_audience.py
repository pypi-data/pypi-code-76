# pylint: skip-file
import ioc

import frf
from frf.lib.test import ProtectedResourceTestCase
from .base import ProtectedResource


class ProtectedResource(ProtectedResource):
    audience = 'foo'


class BearerTokenAudienceTestCase(ProtectedResourceTestCase):
    audience = 'foo'
    base_path = 'test'
    endpoints = [
        (base_path, ProtectedResource)
    ]

    def get_asgi_application(self):
        return frf.get_asgi_application(allowed_hosts=['*'])

    def test_list_returns_200_with_correct_audience(self):
        response = self.request(self.client.get, self.base_path)
        self.assertEqual(response.status_code, 200, response.json())

    def test_list_returns_200_with_correct_audiences(self):
        self.refresh_token(aud=['foo', 'bar', 'baz'])
        response = self.request(self.client.get, self.base_path)
        self.assertEqual(response.status_code, 200, response.json())

    def test_list_returns_403_with_invalid_audience(self):
        self.refresh_token(aud='bar')
        response = self.request(self.client.get, self.base_path)
        self.assertEqual(response.status_code, 403, response.json())

    def test_list_returns_403_with_invalid_audiences(self):
        self.refresh_token(aud=['a', 'b', 'c'])
        response = self.request(self.client.get, self.base_path)
        self.assertEqual(response.status_code, 403, response.json())

