# coding: utf-8
#    COPYRIGHT © 2017. TCPIP.
#    PATENT PENDING. ALL RIGHTS RESERVED.
#    SPEI GATEWAY IS REGISTERED TRADEMARKS OF TCPIP.
#
#    This software is confidential and proprietary information of TCPIP.
#    You shall not disclose such Confidential Information and shall use it only
#    in accordance with the company policy.

"""
     <i>Fecha de creación: 31 de agosto, 2020</i>

     author: Juan Mandujano
     version: 1.0
"""

import unittest

from wire4_auth.auth.oauth_wire4 import OAuthWire4
from wire4_auth.core.environment_enum import EnvironmentEnum
from wire4_client.rest import ApiException


class TokensTest(unittest.TestCase):
    CLIENT_ID: str = "FxUWmqYGZuv8O1qjxstvIyJothMa"
    CLIENT_SECRET: str = "kjwbkrPVgXsnaUGzthj55dsFhx4a"
    USER_KEY: str = "071e2b59b354186b3a0158de493536@sandbox.wire4.mx"
    SECRET_KEY: str = "0d1e33e94604f01b4e00d2fcb6b48f"
    AMBIENT: EnvironmentEnum = EnvironmentEnum.SANDBOX

    def test_givenBadCredentials_should_raisesException(self):
        oauth_wire = OAuthWire4(self.CLIENT_ID, 'self.CLIENT_SECRET', self.AMBIENT)
        with self.assertRaises(ApiException):
            oauth_wire.obtain_access_token_app("general")

    def test_givenValidCredentials_should_returnToken(self):
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)
        token = oauth_wire.obtain_access_token_app("general")
        self.assertIsNotNone(token, "Token shouldn't be None")

    def test_sameCredentials_should_returnSameToken(self):
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)
        first_token = oauth_wire.obtain_access_token_app("general")
        second_token = oauth_wire.obtain_access_token_app("general")
        self.assertEqual(first_token, second_token, "Should be same token")

    def test_givenSomeScopes_should_returnSingleTokenForAllScopes(self):
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)
        token = oauth_wire.obtain_access_token_app("general codi_report")
        self.assertIsNotNone(token, "Token shouldn't be None")

    def test_givenManyTokenWithDifferentScopesForTheSameUser_should_returnAsManyTokenAsScopesRequested(self):
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)
        general_token = oauth_wire.obtain_access_token_app("general")
        report_token = oauth_wire.obtain_access_token_app("codi_report")
        both_tokens = oauth_wire.obtain_access_token_app("general codi_report")
        self.assertNotEqual(general_token, report_token, "Shouldn't be equals")
        self.assertNotEqual(general_token, both_tokens, "Shouldn't be equals")
        self.assertNotEqual(report_token, both_tokens, "Shouldn't be equals")

    def test_givenManyTokenWithDifferentScopesForTheSameUser_should_keepsInCache(self):
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)
        general_token_first = oauth_wire.obtain_access_token_app("general")
        report_token_first = oauth_wire.obtain_access_token_app("codi_report")
        both_tokens_first = oauth_wire.obtain_access_token_app("general codi_report")
        general_token_second = oauth_wire.obtain_access_token_app("general")
        report_token_second = oauth_wire.obtain_access_token_app("codi_report")
        both_tokens_second = oauth_wire.obtain_access_token_app("general codi_report")
        self.assertEquals(general_token_first, general_token_second, 'should be equals')
        self.assertEquals(report_token_first, report_token_second, 'should be equals')
        self.assertEquals(both_tokens_first, both_tokens_second, 'should be equals')

    def test_whenRegenerateToken_should_replaceOldToken(self):
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)
        general_token_first = oauth_wire.obtain_access_token_app("general")
        report_token_first = oauth_wire.obtain_access_token_app("codi_report")
        both_tokens_first = oauth_wire.obtain_access_token_app("general codi_report")
        general_token_second = oauth_wire.obtain_access_token_app("general")
        report_token_second = oauth_wire.obtain_access_token_app("codi_report")
        both_tokens_second = oauth_wire.obtain_access_token_app("general codi_report")
        self.assertEquals(general_token_first, general_token_second, 'should be equals')
        self.assertEquals(report_token_first, report_token_second, 'should be equals')
        self.assertEquals(both_tokens_first, both_tokens_second, 'should be equals')
        general_token_regenerated = oauth_wire.regenerate_access_token_app("general")
        report_token_regenerated = oauth_wire.regenerate_access_token_app("codi_report")
        both_tokens_regenerated = oauth_wire.regenerate_access_token_app("general codi_report")
        self.assertNotEqual(general_token_first, general_token_regenerated, 'should be equals')
        self.assertNotEqual(report_token_first, report_token_regenerated, 'should be equals')
        self.assertNotEqual(both_tokens_first, both_tokens_regenerated, 'should be equals')

    def test_givenBadUserCredentials_should_raisesException(self):
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)
        with self.assertRaises(ApiException):
            oauth_wire.obtain_access_token_app_user(self.USER_KEY, 'self.SECRET_KEY', 'spei_admin')

    def test_givenValidUserCredentials_should_returnToken(self):
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)
        token = oauth_wire.obtain_access_token_app_user(self.USER_KEY, self.SECRET_KEY, 'spei_admin')
        self.assertIsNotNone(token, "Token shouldn't be None")

    def test_sameUserCredentials_should_returnSameToken(self):
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)
        first_token = oauth_wire.obtain_access_token_app_user(self.USER_KEY, self.SECRET_KEY, 'spei_admin')
        second_token = oauth_wire.obtain_access_token_app_user(self.USER_KEY, self.SECRET_KEY, 'spei_admin')
        self.assertEqual(first_token, second_token, "Should be same token")

    def test_givenSomeUserScopes_should_returnSingleTokenForAllScopes(self):
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)
        token = oauth_wire.obtain_access_token_app("spei_admin codi_report")
        self.assertIsNotNone(token, "Token shouldn't be None")

    def test_givenManyTokenWithDifferentScopesForTheSameUserCredentials_should_returnAsManyTokenAsScopesRequested(self):
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)
        spei_admin = oauth_wire.obtain_access_token_app_user(self.USER_KEY, self.SECRET_KEY, 'spei_admin')
        spid_admin = oauth_wire.obtain_access_token_app_user(self.USER_KEY, self.SECRET_KEY, 'spid_admin')
        codi_general = oauth_wire.obtain_access_token_app_user(self.USER_KEY, self.SECRET_KEY, 'codi_general')
        codi_report = oauth_wire.obtain_access_token_app_user(self.USER_KEY, self.SECRET_KEY, 'codi_report')
        self.assertNotEqual(spei_admin, spid_admin, "shouldn't be equals")
        self.assertNotEqual(spei_admin, codi_general, "shouldn't be equals")
        self.assertNotEqual(spei_admin, codi_report, "shouldn't be equals")
        self.assertNotEqual(codi_report, codi_general, "shouldn't be equals")
        self.assertNotEqual(spid_admin, codi_report, "shouldn't be equals")
        self.assertNotEqual(spid_admin, codi_general, "shouldn't be equals")

    def test_givenManyTokenWithDifferentScopesForTheSameUserCredentials_should_keepsInCache(self):
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)
        spei_admin = oauth_wire.obtain_access_token_app_user(self.USER_KEY, self.SECRET_KEY, 'spei_admin')
        spid_admin = oauth_wire.obtain_access_token_app_user(self.USER_KEY, self.SECRET_KEY, 'spid_admin')
        codi_general = oauth_wire.obtain_access_token_app_user(self.USER_KEY, self.SECRET_KEY, 'codi_general')
        codi_report = oauth_wire.obtain_access_token_app_user(self.USER_KEY, self.SECRET_KEY, 'codi_report')
        double_scope = oauth_wire.obtain_access_token_app_user(self.USER_KEY, self.SECRET_KEY,
                                                               'codi_report codi_general')
        spei_admin_second = oauth_wire.obtain_access_token_app_user(self.USER_KEY, self.SECRET_KEY, 'spei_admin')
        spid_admin_second = oauth_wire.obtain_access_token_app_user(self.USER_KEY, self.SECRET_KEY, 'spid_admin')
        codi_general_second = oauth_wire.obtain_access_token_app_user(self.USER_KEY, self.SECRET_KEY, 'codi_general')
        codi_report_second = oauth_wire.obtain_access_token_app_user(self.USER_KEY, self.SECRET_KEY, 'codi_report')
        double_scope_second = oauth_wire.obtain_access_token_app_user(self.USER_KEY, self.SECRET_KEY,
                                                                      'codi_report codi_general')
        self.assertEqual(spei_admin, spei_admin_second, 'should be equals')
        self.assertEqual(spid_admin, spid_admin_second, 'should be equals')
        self.assertEqual(codi_general, codi_general_second, 'should be equals')
        self.assertEqual(codi_report, codi_report_second, 'should be equals')
        self.assertEqual(double_scope, double_scope_second, 'should be equals')

    def test_whenRegenerateTokenForUser_should_replaceOldToken(self):
        oauth_wire = OAuthWire4(self.CLIENT_ID, self.CLIENT_SECRET, self.AMBIENT)
        spei_admin = oauth_wire.obtain_access_token_app_user(self.USER_KEY, self.SECRET_KEY, 'spei_admin')
        spid_admin = oauth_wire.obtain_access_token_app_user(self.USER_KEY, self.SECRET_KEY, 'spid_admin')
        codi_general = oauth_wire.obtain_access_token_app_user(self.USER_KEY, self.SECRET_KEY, 'codi_general')
        codi_report = oauth_wire.obtain_access_token_app_user(self.USER_KEY, self.SECRET_KEY, 'codi_report')
        double_scope = oauth_wire.obtain_access_token_app_user(self.USER_KEY, self.SECRET_KEY,
                                                               'codi_report codi_general')
        spei_admin_second = oauth_wire.regenerate_access_token_app_user(self.USER_KEY, self.SECRET_KEY, 'spei_admin')
        spid_admin_second = oauth_wire.regenerate_access_token_app_user(self.USER_KEY, self.SECRET_KEY, 'spid_admin')
        codi_general_second = oauth_wire.regenerate_access_token_app_user(self.USER_KEY, self.SECRET_KEY,
                                                                          'codi_general')
        codi_report_second = oauth_wire.regenerate_access_token_app_user(self.USER_KEY, self.SECRET_KEY, 'codi_report')
        double_scope_second = oauth_wire.regenerate_access_token_app_user(self.USER_KEY, self.SECRET_KEY,
                                                                          'codi_report codi_general')
        self.assertNotEqual(spei_admin, spei_admin_second, 'should be equals')
        self.assertNotEqual(spid_admin, spid_admin_second, 'should be equals')
        self.assertNotEqual(codi_general, codi_general_second, 'should be equals')
        self.assertNotEqual(codi_report, codi_report_second, 'should be equals')
        self.assertNotEqual(double_scope, double_scope_second, 'should be equals')


if __name__ == '__main__':
    unittest.main()
