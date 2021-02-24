from django.apps import AppConfig
from django.db.models.signals import m2m_changed, post_delete, post_save
from django.apps import apps

class DjangoDiscordConnectorConfig(AppConfig):
    name = 'django_discord_connector'
    package_name = __import__(name).__package_name__
    version = __import__(name).__version__
    verbose_name = 'discord'
    url_slug = 'discord'

    def ready(self):
        from .signals import (user_group_change_sync_discord_groups, 
            remove_discord_user_on_discord_token_removal, 
            sync_discord_groups_on_client_save)

        from django.contrib.auth.models import User
        from django_discord_connector.models import DiscordToken, DiscordClient
        
        m2m_changed.connect(
            user_group_change_sync_discord_groups, sender=User.groups.through)

        post_delete.connect(
            remove_discord_user_on_discord_token_removal,
            sender=DiscordToken
        )

        post_save.connect(
            sync_discord_groups_on_client_save,
            sender=DiscordClient
        )

        if apps.is_installed('packagebinder'):
            from .bindings import create_bindings
            create_bindings()