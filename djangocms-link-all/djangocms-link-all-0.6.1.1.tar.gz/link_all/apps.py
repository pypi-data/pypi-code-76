from django.apps import AppConfig


class LinkAllAppConfig(AppConfig):
    label = 'link_all'
    name = 'link_all'

    def ready(self):
        from link_all.receivers import protect_linked_pages_from_deletion
