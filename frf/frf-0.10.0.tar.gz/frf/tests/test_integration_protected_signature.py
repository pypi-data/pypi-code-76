# pylint: skip-file
import unittest.mock

import ioc
from unimatrix.ext import crypto
from unimatrix.lib.datastructures import DTO

import frf
from frf.lib.test import ProtectedResourceTestCase
from .base import ProtectedResource


class BearerTokenSignatureTestCase(ProtectedResourceTestCase):
    base_path = 'test'
    endpoints = [
        (base_path, ProtectedResource)
    ]

    def get_asgi_application(self):
        return frf.get_asgi_application(allowed_hosts=['*'])

    def test_bearer_with_valid_signature(self):
        self.refresh_token()
        response = self.request(self.client.get, self.base_path + '/me')
        self.assertEqual(response.status_code, 200, response.json())

    def test_bearer_with_invalid_signature(self):
        self.signer.key = crypto.SecretKey({'secret': b'sfsdfs'})
        self.refresh_token(secret='foo') # nosec
        response = self.request(self.client.get, self.base_path + '/me')
        self.assertEqual(response.status_code, 403, response.json())
