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
import datetime
import requests

import webob.dec

import iso8601

from oslo_log import log as logging
from oslo_serialization import jsonutils


class ValidateToken:
    """Validate token middleware

    Fetches the token with the token itself to get it information
    """

    def __init__(self, app, conf):
        self.app = app
        self.conf = conf
        self.logger = logging.getLogger(conf.get('log_name', __name__))

    def _deny_request(self, response=None, message=None):
        """Return error response"""
        if response:
            try:
                body = jsonutils.dumps(response)
            except Exception:
                body = response.text
        elif message:
            body = jsonutils.dumps({'error': {
                'code': 401,
                'title': 'Unauthorized',
                'message': message,
            }})
        resp = webob.Response()
        resp.status = 401
        resp.headers['Content-Type'] = 'application/json'
        resp.body = body.encode()
        return resp

    def __call__(self, environ, start_response):
        self.logger.debug('Entering Validating token auth %s' % environ)
        token = environ.get('HTTP_X_AUTH_TOKEN')
        if token:
            response = requests.request(
                    'GET',
                    '%s/v3/auth/tokens' % self.conf.get('auth_url'),
                    headers={
                        'X-Auth-Token': token,
                        'X-Subject-Token': token
                        }
                    )

            if response.status_code != 200:
                return self._deny_request(
                    jsonutils.dumps(response.json()))(environ, start_response)

            try:
                token_info = response.json().get('token')
                token_expires = token_info.get('expires_at')
                current_time = datetime.datetime.now(datetime.timezone.utc)
                if current_time >= iso8601.parse_date(token_expires):
                    return self._deny_request(
                        message='Token expired')(environ, start_response)
                environ['HTTP_X_IDENTITY_STATUS'] = 'Confirmed'
                environ['keystone.token_info'] = response.json()
                domain = token_info.get('domain')
                if domain:
                    environ['HTTP_X_DOMAIN_ID'] = domain.get('id')
                    environ['HTTP_X_DOMAIN_NAME'] = domain.get('name')
                project = token_info.get('project')
                if project:
                    environ['HTTP_X_PROJECT_ID'] = project.get('id')
                    environ['HTTP_X_PROJECT_NAME'] = project.get('name')
                    pd = project.get('domain')
                    if pd:
                        environ['HTTP_X_PROJECT_DOMAIN_ID'] = pd.get('id')
                        environ['HTTP_X_PROJECT_DOMAIN_NAME'] = pd.get('name')
                user = token_info.get('user')
                if user:
                    environ['HTTP_X_USER_ID'] = user.get('id')
                    environ['HTTP_X_USER_NAME'] = user.get('name')
                    ud = user.get('domain')
                    if ud:
                        environ['HTTP_X_USER_DOMAIN_ID'] = ud.get('id')
                        environ['HTTP_X_USER_DOMAIN_NAME'] = ud.get('name')
                roles = token_info.get('roles')
                if roles:
                    environ['HTTP_X_ROLES'] = ','.join(
                        [f['name'] for f in roles])

            except KeyError:
                return self._deny_request(
                    message='Can not process token data')(
                        environ, start_response)

        return self.app(environ, start_response)


def filter_factory(global_conf, **local_conf):
    """Standard filter factory to use the middleware with paste.deploy"""

    conf = global_conf.copy()
    conf.update(local_conf)

    def auth_filter(app):
        return ValidateToken(app, conf)

    return auth_filter
