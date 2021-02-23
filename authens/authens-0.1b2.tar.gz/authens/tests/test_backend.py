from unittest import mock

from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase

from authens.backends import ENSCASBackend
from authens.models import CASAccount, OldCASAccount
from authens.tests.cas_utils import FakeCASClient

UserModel = get_user_model()


class TestCASBackend(TestCase):
    def test_usernames_uniqueness(self):
        UserModel.objects.create(username="toto")
        UserModel.objects.create(username="toto2")
        backend = ENSCASBackend()
        for _ in range(10):
            username = backend.get_free_username("toto", None)
            self.assertFalse(UserModel.objects.filter(username=username).exists())
            UserModel.objects.create(username=username)
        for _ in range(10):
            username = backend.get_free_username("tutu", None)
            self.assertFalse(UserModel.objects.filter(username=username).exists())
            UserModel.objects.create(username=username)

    def test_email(self):
        backend = ENSCASBackend()
        attributes = {
            "email": "toto@example.com",
            "homeDirectory": "/users/19/info/toto",
        }
        user = backend._get_or_create("toto", attributes)
        self.assertEqual(user.email, "toto@example.com")

    @mock.patch("authens.backends.get_cas_client")
    def test_cas_user_creation(self, mock_cas_client):
        # Make `get_cas_client` return a dummy CAS client for testing purpose.
        fake_cas_client = FakeCASClient()
        mock_cas_client.return_value = fake_cas_client

        # First authentication
        user1 = authenticate(None, ticket="dummy ticket")
        # Should create a user and a Clipper instance.
        self.assertEqual(CASAccount.objects.count(), 1)
        self.assertEqual(UserModel.objects.count(), 1)
        clipper1 = CASAccount.objects.get()
        self.assertEqual(clipper1.user, user1)
        self.assertEqual(clipper1.cas_login, fake_cas_client.cas_login)
        self.assertEqual(clipper1.entrance_year, fake_cas_client.entrance_year)

        # Second time we authenticate the same user.
        user2 = authenticate(None, ticket="dummy ticket")
        # Should return the same user and should not create anything.
        self.assertEqual(CASAccount.objects.count(), 1)
        self.assertEqual(UserModel.objects.count(), 1)
        clipper2 = CASAccount.objects.get()
        self.assertEqual(clipper1, clipper2)
        self.assertEqual(user1, user2)
        self.assertEqual(user2, clipper2.user)

    @mock.patch("authens.backends.get_cas_client")
    def test_name_conflict_handling(self, mock_cas_client):
        # Make `get_cas_client` return a dummy CAS client for testing purpose.
        fake_cas_client = FakeCASClient()
        mock_cas_client.return_value = fake_cas_client

        # Create a regular user (without a CAS account) with the same username as the
        # CAS user before her first login.
        regular_user = UserModel.objects.create_user(username=fake_cas_client.cas_login)

        # First login of the CAS user.
        cas_user = authenticate(None, ticket="dummy ticket")

        self.assertNotEqual(regular_user, cas_user)

    @mock.patch("authens.backends.get_cas_client")
    def test_cas_conflict_handling(self, mock_cas_client):
        # Make `get_cas_client` return a dummy CAS client for testing purpose.
        fake_cas_client = FakeCASClient()
        mock_cas_client.return_value = fake_cas_client

        # Create an old CAS user with the same cas_id as the new CAS user before her
        # first login. This tests the behaviour of the library in the (unlikely)
        # scenario where the SPI decides to give a clipper login that used to be someone
        # else's to a new user.
        old_user = UserModel.objects.create_user(username=fake_cas_client.cas_login)
        old_clipper = CASAccount.objects.create(
            user=old_user,
            cas_login=fake_cas_client.cas_login,
            entrance_year=fake_cas_client.entrance_year - 10,
        )

        # Log the new 'johndoe' in.
        new_user = authenticate(None, ticket="dummy ticket")
        new_clipper = new_user.cas_account

        # Check that it gets a fresh user and a fresh clipper account
        self.assertNotEqual(old_user, new_user)
        self.assertNotEqual(old_clipper, new_clipper)

        # Check that the created CAS account matches the old one
        self.assertEqual(new_clipper.cas_login, fake_cas_client.cas_login)
        self.assertEqual(new_clipper.entrance_year, fake_cas_client.entrance_year)

        # Check deprecation of the old CAS account
        old_user.refresh_from_db()
        self.assertFalse(hasattr(old_user, "cas_account"))
        self.assertTrue(hasattr(old_user, "old_cas_account"))
        old_cas = old_user.old_cas_account
        self.assertEqual(old_cas.cas_login, old_clipper.cas_login)
        self.assertEqual(old_cas.entrance_year, old_clipper.entrance_year)


class TestOldCASBackend(TestCase):
    def test_simple_auth(self):
        user = UserModel.objects.create_user(username="johndoe31", password="password")
        # Decoy user that may be authenticated by mistake
        UserModel.objects.create_user(username="johndoe", password="password")
        OldCASAccount.objects.create(user=user, cas_login="johndoe", entrance_year=2014)

        auth_user = authenticate(
            None, cas_login="johndoe", entrance_year=2014, password="password"
        )
        self.assertEqual(auth_user, user)

    def test_not_migrated_auth(self):
        user = UserModel.objects.create_user(username="vieilleux", password="password")
        CASAccount.objects.create(user=user, cas_login="vieilleux", entrance_year=2015)

        auth_user = authenticate(
            None, cas_login="vieilleux", entrance_year=2015, password="password"
        )
        self.assertEqual(auth_user, user)
