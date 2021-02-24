from django.apps import AppConfig

from .proxy import EtcdProxy


class DjangoInsectConfig(AppConfig):
    name = 'django_insect'

    def ready(self):
        EtcdProxy().run()
