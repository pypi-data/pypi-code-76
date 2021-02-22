# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import copy
import datetime

from unittest import mock

import requests
from requests_mock.contrib import fixture as rm_fixture
import webob

from keystonemiddleware.tests.unit import utils

from validatetoken.middleware import validatetoken


GOOD_RESPONSE = {
    "token": {
        "expires_at": "2021-01-02T00:00:00.00000Z",
        "methods": ["password"],
        "catalog": "<removed>",
        "roles": [
            {"id": "0", "name": "not_admin"},
            {"id": "1", "name": "nova"},
        ],
        "project": {
            "domain": {
                "id": "fake_domain_id",
                "name": "fake_domain_name"
            },
            "id": "fake_project_id",
            "name": "fake_project_name"
        },
        "issued_at": "2021-01-01T00:00:00.000000Z",
        "user": {
            "domain": {
                "id": "fake_user_domain_id",
                "name": "fake_user_domain_name"
            },
            "id": "fake_user_id",
            "name": "fake_user_name",
            "password_expires_at": ""
        }
    }
}


class FakeResponse(object):
    reason = "Test Reason"
    headers = {'x-subject-token': 'fake_token'}

    def __init__(self, json, status_code=400):
        self._json = json
        self.text = json
        self.status_code = status_code

    def json(self):
        return self._json


class FakeApp(object):
    """This represents a WSGI app protected by the auth_token middleware."""

    def __call__(self, env, start_response):
        resp = webob.Response()
        resp.environ = env
        return resp(env, start_response)


class ValidateTokenMiddlewareTestBase(utils.TestCase):
    TEST_AUTH_URL = 'https://keystone.example.com'
    TEST_URL = '%s/v3/auth/tokens' % (TEST_AUTH_URL,)

    def setUp(self):
        super(ValidateTokenMiddlewareTestBase, self).setUp()

        self.conf = {
            'auth_url': self.TEST_AUTH_URL,
        }

        self.requests_mock = self.useFixture(rm_fixture.Fixture())

    def start_fake_response(self, status, headers):
        self.response_status = int(status.split(' ', 1)[0])
        self.response_headers = dict(headers)


class ValidateTokenMiddlewareTestGood(ValidateTokenMiddlewareTestBase):

    def setUp(self):
        super(ValidateTokenMiddlewareTestGood, self).setUp()
        self.middleware = validatetoken.ValidateToken(FakeApp(), self.conf)

        response = copy.deepcopy(GOOD_RESPONSE)
        expires_at = datetime.datetime.now() + datetime.timedelta(hours=1)
        response['token']['expires_at'] = expires_at.isoformat()

        self.requests_mock.get(self.TEST_URL,
                               status_code=200,
                               headers={
                                   'Content-Type': 'application/json'
                               },
                               json=response)

    # Ignore the request and pass to the next middleware in the
    # pipeline if no path has been specified.
    def test_no_path_request(self):
        req = webob.Request.blank('/')
        self.middleware(req.environ, self.start_fake_response)
        self.assertEqual(self.response_status, 200)

    # Ignore the request and pass to the next middleware in the
    # pipeline if no Authorization header has been specified
    def test_without_authorization(self):
        req = webob.Request.blank('/dummy')
        self.middleware(req.environ, self.start_fake_response)
        self.assertEqual(self.response_status, 200)

    @mock.patch.object(requests, 'request')
    def test_token_request(self, mr):
        req = webob.Request.blank('/dummy')
        req.headers['X-Auth-Token'] = 'token'

        mr.return_value = FakeResponse(GOOD_RESPONSE, 200)

        req.get_response(self.middleware)
        mr.assert_called_with(
            'GET',
            'https://keystone.example.com/v3/auth/tokens',
            headers={
                'X-Auth-Token': 'token',
                'X-Subject-Token': 'token'}
        )

    def test_authenticated(self):
        req = webob.Request.blank('/dummy')
        req.headers['X-Auth-Token'] = 'token'

        resp = req.get_response(self.middleware)
        self.assertEqual(resp.status_int, 200)

        token = GOOD_RESPONSE['token']
        env = req.environ
        self.assertEqual(
            'Confirmed',
            env['HTTP_X_IDENTITY_STATUS']
        )
        self.assertEqual(
            token['user']['id'],
            env['HTTP_X_USER_ID']
        )
        self.assertEqual(
            token['user']['name'],
            env['HTTP_X_USER_NAME']
        )

        self.assertEqual(
            token['user']['domain']['id'],
            env['HTTP_X_USER_DOMAIN_ID']
        )
        self.assertEqual(
            token['user']['domain']['name'],
            env['HTTP_X_USER_DOMAIN_NAME']
        )
        self.assertEqual(
            token['project']['id'],
            env['HTTP_X_PROJECT_ID']
        )
        self.assertEqual(
            token['project']['name'],
            env['HTTP_X_PROJECT_NAME']
        )

        self.assertEqual(
            token['project']['domain']['id'],
            env['HTTP_X_PROJECT_DOMAIN_ID']
        )
        self.assertEqual(
            token['project']['domain']['name'],
            env['HTTP_X_PROJECT_DOMAIN_NAME']
        )
        self.assertEqual(
            ','.join([f['name'] for f in token['roles']]),
            env['HTTP_X_ROLES']
        )


class ValidateTokenMiddlewareTestBad(ValidateTokenMiddlewareTestBase):

    def setUp(self):
        super(ValidateTokenMiddlewareTestBad, self).setUp()
        self.middleware = validatetoken.ValidateToken(FakeApp(), self.conf)

        self.requests_mock.get(self.TEST_URL,
                               status_code=200,
                               json=GOOD_RESPONSE)

    def test_token_expired(self):
        req = webob.Request.blank('/dummy')
        req.headers['X-Auth-Token'] = 'token'

        resp = req.get_response(self.middleware)
        self.assertEqual(resp.status_int, 401)

    def test_token_invalid(self):
        self.requests_mock.get(
            self.TEST_URL, status_code=401,
            headers={'Content-Type': 'application/json'},
            json={'error': 'token invalid'})

        req = webob.Request.blank('/dummy')
        req.headers['X-Auth-Token'] = 'token'

        resp = req.get_response(self.middleware)
        self.assertEqual(resp.status_int, 401)
