from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class CASAccount(models.Model):
    """Information about CAS accounts.

    A user is given an instance of this model iff they have a CAS account.

    Instances of this model should only be created by the `ENSCASBackend` authentication
    backend.
    """

    user = models.OneToOneField(
        User,
        verbose_name=_("utilisateurice"),
        on_delete=models.CASCADE,
        related_name="cas_account",
    )
    cas_login = models.CharField(
        verbose_name=_("login CAS"),
        max_length=1023,
        blank=False,
        unique=True,
    )
    entrance_year = models.SmallIntegerField(
        verbose_name=_("année de création du compte CAS"), blank=False, null=False
    )

    class Meta:
        verbose_name = _("Compte CAS")
        verbose_name_plural = _("Comptes CAS")

    def __str__(self):
        return _(
            "compte CAS %(cas_login)s (promo %(entrance_year)s) lié à %(user)s"
        ) % {
            "cas_login": self.cas_login,
            "entrance_year": self.entrance_year,
            "user": self.user.username,
        }


class OldCASAccount(models.Model):
    """Information about expired CAS accounts

    A user is given an instance of this model iff they had a CAS account that expired.

    Instances of this model should not be created with a new user.
    """

    user = models.OneToOneField(
        User,
        verbose_name=_("utilisateurice"),
        on_delete=models.CASCADE,
        related_name="old_cas_account",
    )

    cas_login = models.CharField(
        verbose_name=_("ancien login CAS"), max_length=1023, blank=False
    )

    entrance_year = models.SmallIntegerField(
        verbose_name=_("année de création du compte CAS"), blank=False, null=False
    )

    class Meta:
        # `unique_together` to be deprecated soon : we use `constraints`
        constraints = [
            models.UniqueConstraint(
                fields=["cas_login", "entrance_year"],
                name="clipper_year_uniqueness",
            )
        ]
        verbose_name = _("Ancien compte CAS")
        verbose_name_plural = _("Anciens comptes CAS")

    def __str__(self):
        return _(
            "Ancien compte CAS %(cas_login)s (promo %(entrance_year)s) lié à %(user)s"
        ) % {
            "cas_login": self.cas_login,
            "entrance_year": self.entrance_year,
            "user": self.user.username,
        }
