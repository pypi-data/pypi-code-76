from django import forms
from django.contrib.auth import authenticate, forms as auth_forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def promo_choices():
    return [(r, r) for r in range(2000, timezone.now().year + 1)]


class OldCASAuthForm(forms.Form):
    """Adapts Django's AuthenticationForm to allow for OldCAS login."""

    cas_login = auth_forms.UsernameField(
        label=_("Ancien login clipper"), max_length=1023
    )
    password = forms.CharField(
        label=_("Mot de passe"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
    entrance_year = forms.TypedChoiceField(
        label=_("Promotion"), choices=promo_choices, coerce=int
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cas_login = self.cleaned_data.get("cas_login")
        password = self.cleaned_data.get("password")
        entrance_year = self.cleaned_data.get("entrance_year")

        if cas_login is not None and password:
            self.user_cache = authenticate(
                self.request,
                cas_login=cas_login,
                password=password,
                entrance_year=entrance_year,
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()

        return self.cleaned_data

    def get_user(self):
        # Necessary API for LoginView
        return self.user_cache

    def get_invalid_login_error(self):
        return forms.ValidationError(
            _(
                "Aucun utilisateur n'existe avec ce clipper, cette promo et/ou ce mot "
                "de passe. Veuillez vérifier votre saisie. Attention, tous les champs "
                "sont sensibles à la casse !"
            ),
            code="invalid_login",
        )
