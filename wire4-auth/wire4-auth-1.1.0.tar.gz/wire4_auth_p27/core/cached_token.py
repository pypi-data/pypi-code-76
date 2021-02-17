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
from oauthlib.oauth2 import OAuth2Token


class CachedToken:

    def __init__(self, user_key, user_secret, token):

        self._user_key = user_key
        self._user_secret = user_secret
        self._token = token

    @property
    def user_key(self):

        return self._user_key

    @property
    def user_secret(self):

        return self._user_secret

    @property
    def token(self):

        return self._token

    @token.setter
    def token(self, token):
        self._token = token
