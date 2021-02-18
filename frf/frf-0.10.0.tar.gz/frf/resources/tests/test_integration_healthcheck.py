# pylint: skip-file
from unittest.mock import AsyncMock

import ioc

import frf
from frf.lib.test import ResourceEndpointTestCase

from .. import HealthCheckResource


class HealthCheckResourceTestCase(ResourceEndpointTestCase):
    base_path = 'test'
    endpoints = [
        (base_path, HealthCheckResource)
    ]
    headers = {}

    def setUp(self):
        super().setUp()
        self.svc = ioc.provide('HealthCheckService',
            frf.services.HealthCheckService(),
            force=True)

    def get_asgi_application(self):
        return frf.get_asgi_application(allowed_hosts=['*'])

    def test_live_returns_200(self):
        response = self.request(self.client.get, '/.well-known/health/live')
        self.assertEqual(response.status_code, 200, response.json())

    def test_live_returns_503_on_failure(self):
        self.svc.is_live = AsyncMock(return_value=False)
        response = self.request(self.client.get, '/.well-known/health/live')
        self.assertEqual(response.status_code, 503, response.json())

    def test_live_returns_503_on_exception(self):
        self.svc.is_live = AsyncMock(side_effect=Exception)
        response = self.request(self.client.get, '/.well-known/health/live')
        self.assertEqual(response.status_code, 503, response.json())

    def test_ready_returns_200(self):
        self.svc.is_ready = AsyncMock(return_value=False)
        response = self.request(self.client.get, '/.well-known/health/ready')
        self.assertEqual(response.status_code, 503, response.json())

    def test_ready_returns_503_on_failure(self):
        self.svc.is_ready = AsyncMock(return_value=False)
        response = self.request(self.client.get, '/.well-known/health/ready')
        self.assertEqual(response.status_code, 503, response.json())

    def test_ready_returns_503_on_exception(self):
        self.svc.is_ready = AsyncMock(side_effect=Exception)
        response = self.request(self.client.get, '/.well-known/health/ready')
        self.assertEqual(response.status_code, 503, response.json())
