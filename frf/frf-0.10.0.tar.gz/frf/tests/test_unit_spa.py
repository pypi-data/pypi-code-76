# pylint: skip-file
from unittest.mock import AsyncMock

import ioc
from unimatrix.lib.datastructures import DTO

from ..lib.test import ResourceEndpointTestCase
from ..asgi import get_asgi_application
from ..decorators import spa
from ..views import AnonymousResource


class SinglePageApplication(AnonymousResource):

    @spa('foo.html.j2')
    async def dashboard(self):
        return {'foo': 1, 'bar': 2}


class SinglePageApplicationDecoratorTestCase(ResourceEndpointTestCase):
    base_path = 'test'
    endpoints = [
        (base_path, SinglePageApplication)
    ]

    def setUp(self):
        super().setUp()
        self.svc = DTO(
            render_to_string=AsyncMock(return_value="Hello world!")
        )
        ioc.provide('TemplateService', self.svc)

    def get_asgi_application(self):
        return get_asgi_application(allowed_hosts=['*'])

    def test_template_service_is_invoked(self):
        response = self.client.get('test/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Hello world!")
