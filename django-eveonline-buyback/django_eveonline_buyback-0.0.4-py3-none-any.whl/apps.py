from django.apps import AppConfig


class DjangoEveonlineBuybackConfig(AppConfig):
    name = 'django_eveonline_buyback'
    verbose_name = 'EVE Online Buyback Tool'
    url_slug = 'eveonline'
    package_name = __import__(name).__package_name__
    version = __import__(name).__version__

    def ready(self):
        from .bindings import create_bindings
        create_bindings()