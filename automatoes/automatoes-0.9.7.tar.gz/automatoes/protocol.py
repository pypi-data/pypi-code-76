#!/usr/bin/env python
#
# Copyright 2019-2020 Flavio Goncalves Garcia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from . import get_version
from .crypto import (export_certificate_for_acme, generate_header, jose_b64,
                     sign_request, sign_request_v2)
from peasant.client import Peasant, PeasantTransport
import requests


class AcmeTransport(PeasantTransport):

    def __init__(self):
        self._default_header = {
            'User-Agent': ("automatoes %s (https://candango.org/p/automatoes)"
                           % get_version())
        }

    def set_directory(self):
        raise NotImplementedError

    def new_nonce(self):
        raise NotImplementedError

    def get(self, path, **kwargs):
        headers = kwargs.get("headers")
        verify = kwargs.get("verify")
        _headers = self._default_header.copy()
        if headers:
            _headers.update(headers)
        kwargs = {
            'headers': _headers
        }

        if verify:
            kwargs['verify'] = self.verify

        return requests.get(self.path(path), **kwargs)

    def head(self, path, **kwargs):
        raise NotImplementedError

    def post(self, path, body, **kwargs):
        headers = kwargs.get("headers")
        kid = kwargs.get("kid")
        verify = kwargs.get("verify")
        _headers = self._default_header.copy()
        _headers['Content-Type'] = "application/jose+json"
        if headers:
            _headers.update(headers)

        protected = self.get_headers(url=self.path(path))
        if kid:
            protected['kid'] = kid
            protected.pop('jwk')
        body = sign_request_v2(self.account.key, protected, body)
        kwargs = {
            'headers': _headers
        }
        if self.verify:
            kwargs['verify'] = self.verify
        return requests.post(self.path(path), data=body, **kwargs)

    def post_as_get(self, path, **kwargs):
        headers = kwargs.get("headers")
        kid = kwargs.get("kid")
        _headers = DEFAULT_HEADERS.copy()
        _headers['Content-Type'] = "application/jose+json"
        if headers:
            _headers.update(headers)

        protected = self.get_headers(url=self.path(path))
        protected['kid'] = kid
        protected.pop('jwk')
        body = sign_request_v2(self.account.key, protected, None)
        kwargs = {
            'headers': _headers
        }
        if self.verify:
            kwargs['verify'] = self.verify
        return requests.post(self.path(path), data=body, **kwargs)


class AcmePeasant(Peasant):

    def __init__(self, transport):
        super(AcmePeasant, self).__init__(transport)
        self._prior_version = 1
        self._version = 2

