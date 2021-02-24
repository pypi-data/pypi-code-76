server_type = 'dictionary'

server_type = 'feeds'

import requests
import time


class GracieSSOAuthError(Exception):
    def __init__(self, message, *args):
        self.message = message
        self.args = args

    def __str__(self):
        return repr(self.message)


class GracieSSOAuth(requests.Session):
    _sso_server = None
    _session_information = None
    _basic_auth_key = 'Y2xpZW50X0RFUzpwYXNzMDlzOGQwOXcx'
    _login_name = None
    _login_password = None
    _verify_ssl = None

    def __init__(self, sso_host, login_name, login_password, verify_ssl):
        super(GracieSSOAuth, self).__init__()
        self._sso_server = '%s/oauth/token' % sso_host
        self._login_name = login_name
        self._login_password = login_password
        self._verify_ssl = verify_ssl

    def login(self, login_name=None, login_password=None):
        if not login_name:
            login_name = self._login_name
        if not login_password:
            login_password = self._login_password

        payload = {'username': login_name,
                   'password': login_password,
                   'grant_type': 'password',
                   'scope': 'api:default_access'}
        headers = {'Authorization': 'Basic %s' % self._basic_auth_key}
        response = self.post(self._sso_server, data=payload, headers=headers, verify=self._verify_ssl)
        if response.status_code != 200:
            raise GracieSSOAuthError('%s error authenticating to SSO server: %s' % (response.status_code, response.text))
        self._session_information = response.json()
        self._session_information['expire_time'] = self._session_information['expires_in'] + int(time.time())
        return response.status_code

    @property
    def basic_auth_key(self):
        return self._basic_auth_key

    @basic_auth_key.setter
    def basic_auth_key(self, auth_key):
        self._basic_auth_key = auth_key

    @property
    def access_token(self):
        return self.access_info['access_token']

    @property
    def access_info(self):
        # if session is not set or the token has expired login
        if not self._session_information or ('expire_time' in self._session_information and (
                self._session_information['expire_time'] - int(time.time()) <= 60)):
            self.login(self._login_name, self._login_password)
        return self._session_information

    @property
    def access_headers(self):
        return {'authorization': '%s %s' % (self.access_info['token_type'].capitalize(),
                                             self.access_info['access_token'])}
