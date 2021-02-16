#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2020 FABRIC Testbed
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#
# Author: Komal Thareja (kthare10@renci.org)
from fabric_cm.credmgr import swagger_client
from fabric_cm.credmgr.swagger_client.rest import ApiException as CredMgrException


class CredmgrProxy:
    """
    Credential Manager Proxy
    """
    def __init__(self, credmgr_host: str):
        self.host = credmgr_host
        self.tokens_api = None
        if credmgr_host is not None:
            # create an instance of the API class
            configuration = swagger_client.configuration.Configuration()
            configuration.host = f"https://{credmgr_host}/"
            api_instance = swagger_client.ApiClient(configuration)
            self.tokens_api = swagger_client.TokensApi(api_client=api_instance)
            self.default_api = swagger_client.DefaultApi(api_client=api_instance)

    def refresh(self, project_name: str, scope: str, refresh_token: str) -> dict:
        """
        Refresh token
        @param project_name project name
        @param scope scope
        @param refresh_token refresh token
        @returns the dictionary containing the tokens
        @raises Exception in case of failure
        """
        try:
            body = swagger_client.Request(refresh_token)
            api_response = self.tokens_api.tokens_refresh_post(body=body,
                                                               project_name=project_name,
                                                               scope=scope)

            return api_response.to_dict()

        except CredMgrException as e:
            raise Exception(e.reason, e.body)

    def revoke(self, refresh_token: str) -> str:
        """
        Revoke token
        @param refresh_token refresh token
        @returns response
        @raises Exception in case of failure
        """
        try:
            body = swagger_client.Request(refresh_token)
            api_response = self.tokens_api.tokens_revoke_post(body=body)

            return api_response.to_dict()
        except CredMgrException as e:
            raise Exception(e.reason, e.body)

    def certs_get(self):
        """
        Return certificates
        """
        try:
            return self.default_api.certs_get()
        except CredMgrException as e:
            raise Exception(e.reason, e.body)

    def version_get(self):
        """
        Return Version
        """
        try:
            return self.default_api.version_get()
        except CredMgrException as e:
            raise Exception(e.reason, e.body)
