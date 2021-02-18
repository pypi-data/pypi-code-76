# pylint: skip-file
import asyncio

from unimatrix.ext.jose.tests.const import RSA_KEY
from unimatrix.ext import crypto
from unimatrix.ext import jose

import frf
from ..lib.test import ProtectedResourceTestCase
from .base import ProtectedResource


A = lambda *args, **kwargs: asyncio.run(*args, **kwargs)


class BearerTokenResolvedKeyValidationTestCase(ProtectedResourceTestCase):
    base_path = 'test'
    endpoints = [
        (base_path, ProtectedResource)
    ]

    def setUp(self):
        self.key = RSA_KEY
        crypto.chain.register(self.key.id, self.key)
        crypto.trust.register(self.key.id, A(self.key.get_public_key()))
        super().setUp()

    def get_signer(self):
        return crypto.get_signer(
            algorithm=crypto.algorithms.RSAPKCS1v15SHA256,
            keyid=self.key.id
        )

    def tearDown(self):
        crypto.chain.keys.pop(self.key.id)
        crypto.trust.keys.pop(self.key.id)

    def get_asgi_application(self):
        return frf.get_asgi_application(allowed_hosts=['*'])

    def test_no_authorization_header_returns_401(self):
        response = self.client.get('/test')
        self.assertEqual(response.status_code, 401)

        dto = response.json()
        self.assertIn('code', dto)
        self.assertEqual(dto['code'], 'BEARER_TOKEN_MISSING')

    def test_authorization_with_valid_token(self):
        response = self.client.get('/test', headers=self.headers)
        self.assertEqual(response.status_code, 200, msg=response.json())
