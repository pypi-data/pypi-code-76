# pylint: skip-file
import frf
from frf.lib.test import ResourceEndpointTestCase


class AnonymousResource(frf.AnonymousResource):

    async def list(self):
        return {}


class AnonymousResourceTestCase(ResourceEndpointTestCase):
    base_path = 'test'
    endpoints = [
        (base_path, AnonymousResource)
    ]

    def get_asgi_application(self):
        return frf.get_asgi_application(allowed_hosts=['*'])

    def test_list_returns_200(self):
        response = self.client.get(self.base_path)
        self.assertEqual(response.status_code, 200, response.json())
