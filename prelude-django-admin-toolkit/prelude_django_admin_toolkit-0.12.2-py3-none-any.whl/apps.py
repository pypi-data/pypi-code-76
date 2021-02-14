from django.contrib.admin.apps import AdminConfig

"""
import pathlib
from django.conf import settings 

prelude_django_admin_toolkit_locale = pathlib.Path(__file__).parent.absolute() / 'locale'

locale_paths = getattr(settings, 'LOCALE_PATHS', [])

locale_paths += [
    prelude_django_admin_toolkit_locale,
]
"""


class PrlAdminConfig(AdminConfig):
    default_site = 'prelude_django_admin_toolkit.admin.PrlAdmin'
