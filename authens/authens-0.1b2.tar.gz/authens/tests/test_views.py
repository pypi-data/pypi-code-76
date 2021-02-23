from unittest.mock import patch
from urllib.parse import quote

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.test import Client, TestCase
from django.urls import reverse

from authens.models import CASAccount, OldCASAccount
from authens.tests.cas_utils import FakeCASClient

UserModel = get_user_model()


class TestLoginViews(TestCase):
    def test_cas_login_redirect(self):
        url = reverse("authens:login.cas")
        abs_url = "http://testserver{}".format(url)
        client = Client()

        # User request without ticket: redirect to the CAS login page.
        response = client.get(url)
        self.assertRedirects(
            response,
            "https://cas.eleves.ens.fr/login?service={}".format(quote(abs_url)),
            fetch_redirect_response=False,
        )

    @patch("authens.backends.get_cas_client")
    def test_cas_login_with_ticket(self, mock_cas_client):
        # Make `get_cas_client` return a dummy CAS client that skips ticket verification
        # and always log in a user with CAS login 'johndoe'.
        mock_cas_client.return_value = FakeCASClient()

        url = reverse("authens:login.cas")
        client = Client()

        # User request with a CAS ticket: validate the ticket.
        response = client.get("{}?ticket=dummy-ticket".format(url), follow=True)
        self.assertRedirects(response, settings.LOGIN_REDIRECT_URL)

    def test_can_gen_login_switch(self):
        response = Client().get(reverse("authens:login"))
        self.assertEqual(response.status_code, 200)

    def test_oldcas_login(self):
        url = reverse("authens:login.oldcas")
        client = Client()

        user = UserModel.objects.create_user(username="johndoe31", password="password")
        # Decoy user that may be authenticated by mistake
        UserModel.objects.create_user(username="johndoe", password="password")
        OldCASAccount.objects.create(user=user, cas_login="johndoe", entrance_year=2014)

        post_data = dict(cas_login="johndoe", password="password", entrance_year=2014)
        response = client.post(url, post_data)
        self.assertRedirects(response, settings.LOGIN_REDIRECT_URL)

    def test_oldcas_login_error(self):
        url = reverse("authens:login.oldcas")
        client = Client()

        user = UserModel.objects.create_user(username="johndoe31", password="password")
        OldCASAccount.objects.create(user=user, cas_login="johndoe", entrance_year=2014)

        wrong_year = dict(cas_login="johndoe", password="password", entrance_year=2015)
        wrong_login = dict(
            cas_login="johndoe31", password="password", entrance_year=2014
        )

        response = client.post(url, wrong_year, follow=True)
        non_field_errors = response.context["form"].non_field_errors().as_data()
        self.assertEqual(non_field_errors[0].code, "invalid_login")

        response = client.post(url, wrong_login, follow=True)
        non_field_errors = response.context["form"].non_field_errors().as_data()
        self.assertEqual(non_field_errors[0].code, "invalid_login")


class TestLogoutView(TestCase):
    def test_regular_logout(self):
        # Regular user (without a CAS account)
        user = UserModel.objects.create_user(username="johndoe")

        # Log the user in
        client = Client()
        client.force_login(user)

        self.assertEqual(Session.objects.count(), 1)
        response = client.get("/authens/logout")
        self.assertEqual(Session.objects.count(), 0)  # User is actually logged out.
        self.assertRedirects(response, settings.LOGOUT_REDIRECT_URL)

    @patch("authens.backends.get_cas_client")
    def test_cas_logout(self, mock_cas_client):
        # Make `get_cas_client` return a dummy CAS client that skips ticket verification
        # and always log in a user with CAS login 'johndoe'.
        # This is only used for login.
        mock_cas_client.return_value = FakeCASClient()

        # CAS user
        user = UserModel.objects.create_user(username="johndoe")
        CASAccount.objects.create(user=user, cas_login="johndoe", entrance_year=2019)

        # Log the user in via CAS
        client = Client()
        client.get("/authens/login/cas?ticket=dummy-ticket")

        self.assertEqual(Session.objects.count(), 1)
        response = client.get("/authens/logout")
        self.assertEqual(Session.objects.count(), 0)  # User is logged out…
        self.assertRedirects(  # … and redirected to the CAS logout page.
            response,
            "https://cas.eleves.ens.fr/logout?service={}".format(
                quote("http://testserver/public")
            ),
            fetch_redirect_response=False,
        )

    def test_regular_logout_on_cas_account(self):
        # CAS user
        user = UserModel.objects.create_user(username="johndoe", password="p4ssw0rd")
        CASAccount.objects.create(user=user, cas_login="johndoe", entrance_year=2019)

        # Log the user in by password and *not* via CAS
        client = Client()
        client.login(username="johndoe", password="p4ssw0rd")

        self.assertEqual(Session.objects.count(), 1)
        response = client.get("/authens/logout")
        self.assertEqual(Session.objects.count(), 0)  # User is logged out…
        # … and not redirected to the CAS logout page.
        self.assertRedirects(response, settings.LOGOUT_REDIRECT_URL)
