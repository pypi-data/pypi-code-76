#    COPYRIGHT © 2017. TCPIP.
#    PATENT PENDING. ALL RIGHTS RESERVED.
#    SPEI GATEWAY IS REGISTERED TRADEMARKS OF TCPIP.
#
#    This software is confidential and proprietary information of TCPIP.
#    You shall not disclose such Confidential Information and shall use it only
#    in accordance with the company policy.

# coding: utf-8

"""
     <i>Fecha de creación: 5 de diciembre, 2019</i>

     author: Saintiago García
     version: 1.0
"""

import os
from collections import OrderedDict
from datetime import datetime, timedelta

from oauthlib.oauth2 import BackendApplicationClient, LegacyApplicationClient
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

from wire4_client import ApiClient
from wire4_client.configuration import Configuration
from wire4_client.rest import ApiException

from wire4_auth_p27.core.cached_token import CachedToken
from wire4_auth_p27.core.environment_enum import EnvironmentEnum


class OAuthWire4:

    MAX_APP_USER_SIZE_CACHED = 100

    def __init__(self, client_id, client_secret, environment=EnvironmentEnum.SANDBOX):
        os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "True"
        self._client_id = client_id
        self._client_secret = client_secret
        self._environment = environment

        if self._environment is None:
            self._environment = EnvironmentEnum.SANDBOX

        # noinspection PyTypeChecker
        self._token_cached_app = CachedToken(None, None, None)
        self._tokens_cached_app_user = OrderedDict()

    def obtain_access_token_app(self, scope="general"):

        if self._token_cached_app.token is not None and scope in self._token_cached_app.token.get("scope") and \
                self.__is_expired(self._token_cached_app.token.get("expires_at")) and \
                self._token_cached_app.token.get("access_token") is not None:

            return self.__format_to_header(self._token_cached_app.token.get("access_token"))

        try:
            auth = HTTPBasicAuth(self._client_id, self._client_secret)
            scopes = [scope]
            client = BackendApplicationClient(client_id=self._client_id, scope=scopes)

            oauth = OAuth2Session(client=client)
            token = oauth.fetch_token(token_url=self._environment.token_url, auth=auth)
            self._token_cached_app.token = token

            return self.__format_to_header(token.get("access_token"))
        except Exception as ex:
            raise ApiException(reason="error to obtain token app: {0}".format(ex))

    def obtain_access_token_app_user(self, user_key, secret_key, scope="spei_admin"):

        key_search = user_key + scope
        token_cached = self.tokens_cached_app_user.get(key_search)
        if token_cached is not None and scope in token_cached.token.get("scope") and \
                self.__is_expired(token_cached.token.get("expires_at")) and \
                token_cached.token.get("access_token") is not None:

            return self.__format_to_header(token_cached.token.get("access_token"))

        try:
            auth = HTTPBasicAuth(self._client_id, self._client_secret)
            scopes = [scope]
            client = LegacyApplicationClient(client_id=self._client_id)

            oauth = OAuth2Session(client=client)
            token = oauth.fetch_token(token_url=self._environment.token_url, username=user_key,
                                      password=secret_key, auth=auth, scope=scopes)

            if len(self._tokens_cached_app_user) + 1 > self.MAX_APP_USER_SIZE_CACHED:
                for key in self._tokens_cached_app_user:
                    self._tokens_cached_app_user.pop(key)
                    break

            self._tokens_cached_app_user[key_search] = CachedToken(user_key, secret_key, token)

            return self.__format_to_header(token.get("access_token"))
        except Exception as ex:
            raise ApiException(reason="error to obtain token app user: {0}".format(ex))

    def regenerate_access_token_app(self, scope="general"):

        try:
            auth = HTTPBasicAuth(self._client_id, self._client_secret)
            scopes = [scope]
            client = BackendApplicationClient(client_id=self._client_id, scope=scopes)

            oauth = OAuth2Session(client=client)
            token = oauth.fetch_token(token_url=self._environment.token_url, auth=auth)
            self._token_cached_app.token = token

            return self.__format_to_header(token.get("access_token"))
        except Exception as ex:
            raise ApiException(reason="error to obtain token app: {0}".format(ex))

    def regenerate_access_token_app_user(self, user_key, secret_key, scope="spei_admin"):

        key_search = user_key + scope
        try:
            auth = HTTPBasicAuth(self._client_id, self._client_secret)
            scopes = [scope]
            client = LegacyApplicationClient(client_id=self._client_id)

            oauth = OAuth2Session(client=client)
            token = oauth.fetch_token(token_url=self._environment.token_url, username=user_key,
                                      password=secret_key, auth=auth, scope=scopes)

            if len(self._tokens_cached_app_user) + 1 > self.MAX_APP_USER_SIZE_CACHED:
                for key in self._tokens_cached_app_user:
                    self._tokens_cached_app_user.pop(key)
                    break

            self._tokens_cached_app_user[key_search] = CachedToken(user_key, secret_key, token)

            return self.__format_to_header(token.get("access_token"))
        except Exception as ex:
            raise ApiException(reason="error to obtain token app user: {0}".format(ex))

    def __is_expired(self, expires_at):

        return expires_at is not None and datetime.fromtimestamp(expires_at) > (datetime.now() - timedelta(minutes=5))

    def __format_to_header(self, token):

        return "Bearer " + token

    def get_default_api_client(self):
        # Configure OAuth2 access token for authorization
        configuration = Configuration()
        configuration.host = self._environment.service_url

        return ApiClient(configuration)
