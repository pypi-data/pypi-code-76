# pylint: skip-file
import ioc

import frf
from frf.lib.test import ProtectedResourceTestCase
from .base import ProtectedResource


class ProtectedResource(ProtectedResource):
    required_scopes = ['foo', 'bar']


class BearerTokenScopesTestCase(ProtectedResourceTestCase):
    base_path = 'test'
    endpoints = [
        (base_path, ProtectedResource)
    ]

    def get_asgi_application(self):
        return frf.get_asgi_application(allowed_hosts=['*'])

    def test_list_returns_200_with_correct_scopes_equal(self):
        self.refresh_token(scopes=['foo', 'bar'])
        response = self.request(self.client.get, self.base_path)
        self.assertEqual(response.status_code, 200, response.json())

    def test_list_returns_200_with_correct_scopes_superset(self):
        self.refresh_token(scopes=['foo', 'bar', 'baz'])
        response = self.request(self.client.get, self.base_path)
        self.assertEqual(response.status_code, 200, response.json())

    def test_list_returns_403_with_invalid_scope_subset(self):
        self.refresh_token(scopes=['foo'])
        response = self.request(self.client.get, self.base_path)
        self.assertEqual(response.status_code, 401, response.json())

    def test_list_returns_403_with_invalid_scope_missing(self):
        self.refresh_token()
        response = self.request(self.client.get, self.base_path)
        self.assertEqual(response.status_code, 401, response.json())

    def test_list_returns_403_with_invalid_scope_disjoint(self):
        self.refresh_token(scopes=['taz'])
        response = self.request(self.client.get, self.base_path)
        self.assertEqual(response.status_code, 401, response.json())
