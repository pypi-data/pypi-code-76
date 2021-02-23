from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class LanguageToolsConfig(AppConfig):
    name = 'ok_language_tools'
    verbose_name = _('Language tools')
