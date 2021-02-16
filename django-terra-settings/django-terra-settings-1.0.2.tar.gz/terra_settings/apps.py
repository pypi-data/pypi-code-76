from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy as _

if "terra_accounts" in settings.INSTALLED_APPS:

    from terra_accounts.permissions_mixins import PermissionRegistrationMixin

    class TerraSettingsConfig(PermissionRegistrationMixin, AppConfig):
        name = "terra_settings"

        permissions = (
            ("BaseLayer", "can_manage_baselayers", _("Can manage base map layers")),
        )


else:

    class TerraSettingsConfig(AppConfig):
        name = "terra_settings"
