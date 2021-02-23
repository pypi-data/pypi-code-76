from urllib.parse import urlparse, urlunparse

from django.conf import settings
from django.contrib import auth
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, View

from authens import conf as default_conf
from authens.forms import OldCASAuthForm
from authens.utils import get_cas_client


class NextPageMixin:
    def get_next_url(self):
        """Decide where to go after a successful login.

        Look for (in order):
        - a `next` GET parameter;
        - a `CASNEXT` session variable;
        - the `LOGIN_REDIRECT_URL` django setting.
        """
        request = self.request
        next_url = request.GET.get("next")
        if next_url is None and "CASNEXT" in request.session:
            next_url = request.session["CASNEXT"]
            del request.session["CASNEXT"]
        if next_url is None:
            next_url = settings.LOGIN_REDIRECT_URL
        return str(next_url)


class LoginSwitchView(NextPageMixin, TemplateView):
    """Simple page letting the user choose between password and CAS authentication."""

    template_name = "authens/login_switch.html"
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_next_url())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx.update(
            {
                "next": self.get_next_url(),
                "oldcas": getattr(
                    settings, "AUTHENS_USE_OLDCAS", default_conf.AUTHENS_USE_OLDCAS
                ),
            }
        )
        return ctx


class CASLoginView(NextPageMixin, View):
    """CAS authentication view.

    Implement the CAS authentication scheme:

    1. We first redirect the user to the student CAS.
    2. The user comes back with a ticket, we validate it to make sure the user is legit
       (validation is delegated to the ENSCASBackend).
    3. We redirect the user to the next page.
    """

    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        ticket = request.GET.get("ticket")

        if not ticket:
            request.session["CASNEXT"] = self.get_next_url()
            cas_client = get_cas_client(request)
            return redirect(cas_client.get_login_url())

        user = auth.authenticate(request, ticket=ticket)
        if user is None:
            raise PermissionDenied(_("Connection échouée !"))
        auth.login(request, user)
        return redirect(self.get_next_url())


class PasswordLoginView(auth_views.LoginView):
    template_name = "authens/pwd_login.html"


class PasswordResetView(SuccessMessageMixin, auth_views.PasswordResetView):
    template_name = "authens/pwd_reset.html"
    email_template_name = "authens/pwd_reset_email.txt"
    subject_template_name = "authens/pwd_reset_subject.txt"
    success_url = reverse_lazy("authens:login")

    success_message = _(
        "Un email de réinitialisation vient d'être envoyé à l'adresse indiquée !"
    )


class PasswordResetConfirmView(
    SuccessMessageMixin, auth_views.PasswordResetConfirmView
):
    template_name = "authens/pwd_reset_confirm.html"
    success_url = reverse_lazy("authens:login")

    success_message = _("Mot de passe modifié avec succès !")


class OldCASLoginView(auth_views.LoginView):
    template_name = "authens/oldcas_login.html"
    authentication_form = OldCASAuthForm

    def get_initial(self):
        return {"entrance_year": timezone.now().year - 5}


class LogoutView(auth_views.LogoutView):
    """Logout view of AuthENS.

    Tell Django to log the user out, then redirect to the CAS logout page if the user
    logged in via CAS.
    """

    def setup(self, request):
        super().setup(request)
        if "CASCONNECTED" in request.session:
            del request.session["CASCONNECTED"]
            self.cas_connected = True
        else:
            self.cas_connected = False

    def get_next_page(self):
        next_page = super().get_next_page()
        if self.cas_connected:
            cas_client = get_cas_client(self.request)

            # If the next_url is local (no hostname), make it absolute so that the user
            # is correctly redirected from CAS.
            if not urlparse(next_page).netloc:
                request = self.request
                next_page = urlunparse(
                    (request.scheme, request.get_host(), next_page, "", "", "")
                )

            next_page = cas_client.get_logout_url(redirect_url=next_page)
        return next_page
