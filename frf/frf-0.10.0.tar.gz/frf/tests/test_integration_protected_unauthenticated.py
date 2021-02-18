# pylint: skip-file
import frf
from frf.lib.test import ResourceEndpointTestCase


class ProtectedResource(frf.Resource):

    async def list(self):
        return {}


class ProtectedResourceTestCase(ResourceEndpointTestCase):
    base_path = 'test'
    endpoints = [
        (base_path, ProtectedResource)
    ]

    def get_asgi_application(self):
        return frf.get_asgi_application(allowed_hosts=['*'])

    def test_list_returns_403(self):
        response = self.client.get(self.base_path)
        self.assertEqual(response.status_code, 401, response.json())

    def test_list_returns_bearer_token_missing(self):
        response = self.client.get(self.base_path)
        dto = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertIn('code', dto, dto)
        self.assertEqual(dto['code'], 'BEARER_TOKEN_MISSING')
