# pylint: skip-file
import ioc

import frf
from frf.lib.test import ProtectedResourceTestCase
from .base import ProtectedResource


class MinimalBearerTokenTestCase(ProtectedResourceTestCase):
    base_path = 'test'
    endpoints = [
        (base_path, ProtectedResource)
    ]

    def get_asgi_application(self):
        return frf.get_asgi_application(allowed_hosts=['*'])

    def test_list_returns_200(self):
        response = self.request(self.client.get, self.base_path)
        self.assertEqual(response.status_code, 200, response.json())
