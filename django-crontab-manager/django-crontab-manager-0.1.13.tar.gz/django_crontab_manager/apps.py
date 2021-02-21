from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class DjangoCrontabManagerConfig(AppConfig):
    name = 'django_crontab_manager'
    verbose_name = _("Django Crontab Manager")
