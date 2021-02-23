from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase

from authens.models import CASAccount, OldCASAccount
from authens.shortcuts import register_cas_account
from authens.tests.cas_utils import FakeLDAPObject

User = get_user_model()


class TestRegisterCasAccount(TestCase):
    @mock.patch("authens.shortcuts.ldap.initialize")
    def test_register(self, mock_ldap_obj):
        mock_ldap_obj.return_value = FakeLDAPObject("johndoe", 2019)

        user = User.objects.create_user(username="whatever")
        self.assertFalse(hasattr(user, "cas_account"))

        register_cas_account(user, cas_login="johndoe")
        user.refresh_from_db()
        self.assertTrue(hasattr(user, "cas_account"))
        self.assertEqual(user.cas_account.cas_login, "johndoe")
        self.assertEqual(user.cas_account.entrance_year, 2019)

    def test_cant_register_twice(self):
        john = User.objects.create_user(username="whatever")
        CASAccount.objects.create(user=john, cas_login="johndoe", entrance_year=2019)

        janis = User.objects.create_user(username="janisjoplin")

        # John cannot have two CAS accounts
        with self.assertRaises(ValueError):
            register_cas_account(john, cas_login="joplin")

        # Janis cannot steal John's account
        with self.assertRaises(ValueError):
            register_cas_account(janis, cas_login="johndoe")

        self.assertEqual(CASAccount.objects.count(), 1)

    def test_cant_register_old_account(self):
        user = User.objects.create_user(username="whatever")
        OldCASAccount.objects.create(user=user, cas_login="toto", entrance_year=2012)

        with self.assertRaises(ValueError):
            register_cas_account(user, cas_login="toto")

        self.assertFalse(CASAccount.objects.exists())
