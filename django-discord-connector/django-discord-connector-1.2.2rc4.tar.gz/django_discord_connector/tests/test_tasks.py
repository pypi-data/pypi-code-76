from unittest.mock import patch
from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User, Group
from django_discord_connector.models import DiscordUser, DiscordGroup, DiscordToken, DiscordClient
from django_discord_connector.tasks import *
import django_discord_connector


def mock_discord_task(args=None, countdown=None):
    pass


class MockDiscordResponse():
    def __init__(self, status_code, response={}):
        self.status_code = status_code
        self.response = response

    def json(self):
        return self.response


class TestDiscordTaskSuite(TransactionTestCase):
    def setUp(self):
        print(self._testMethodName)
        from django_discord_connector.signals import (
            user_group_change_sync_discord_groups,
            remove_discord_user_on_discord_token_removal,
            sync_discord_groups_on_client_save)

        from django.db.models.signals import (
            m2m_changed,
            post_delete,
            post_save)

        from django.contrib.auth.models import User
        from django_discord_connector.models import DiscordToken, DiscordClient
        m2m_changed.disconnect(
            user_group_change_sync_discord_groups, sender=User.groups.through)

        post_delete.disconnect(
            remove_discord_user_on_discord_token_removal,
            sender=DiscordToken
        )
        post_save.disconnect(
            sync_discord_groups_on_client_save,
            sender=DiscordClient
        )
        DiscordClient.objects.create(
            callback_url="https://localhost:8000",
            server_id="1",
            client_id="1",
            client_secret="null",
            bot_token="null",
            invite_link="https://localhost",
        )
        self.group = Group.objects.create(
            name="Group"
        )

        self.user = User.objects.create(
            username="test"
        )

        self.discord_user = DiscordUser.objects.create(
            username="test",
            nickname="test",
            external_id=1,
        )

        self.no_token_discord_user = DiscordUser.objects.create(
            username="notoken",
            nickname="notoken",
            external_id=2,
        )

        self.discord_token = DiscordToken.objects.create(
            access_token="null",
            refresh_token="null",
            discord_user=self.discord_user,
            user=self.user
        )

        self.discord_group = DiscordGroup.objects.create(
            name="DiscordGroup",
            external_id=1,
            group=self.group
        )

    def tearDown(self):
        User.objects.all().delete()
        Group.objects.all().delete()
        DiscordToken.objects.all().delete()
        DiscordUser.objects.all().delete()
        DiscordGroup.objects.all().delete()

    @patch('django_discord_connector.tasks.remove_discord_user.apply_async')
    @patch('django_discord_connector.tasks.update_discord_user.apply_async')
    @patch('django_discord_connector.tasks.DiscordRequest.remove_role_from_user')
    def test_sync_all_discord_users_accounts(self, mock_discord_call, mock_discord_update_task, mock_discord_remove_task):
        self.assertEqual(DiscordUser.objects.all().count(), 2)
        mock_discord_call.return_value = MockDiscordResponse(status_code=204)
        # assuming update is tested elsewhere
        mock_discord_update_task.return_value = None
        mock_discord_remove_task.side_effect = remove_discord_user(
            self.no_token_discord_user.external_id)
        sync_all_discord_users_accounts()
        self.assertEqual(DiscordUser.objects.all().count(), 1)

    @patch('django_discord_connector.tasks.DiscordRequest.remove_role_from_user')
    def test_remove_user(self, mock_discord_call):
        external_id = self.discord_user.external_id
        mock_discord_call.return_value = MockDiscordResponse(status_code=204)
        remove_discord_user(self.discord_user.external_id)
        self.assertFalse(DiscordUser.objects.filter(
            external_id=external_id).exists())

    @patch('django_discord_connector.tasks.DiscordRequest.remove_role_from_user')
    def test_remove_user_failure_user_still_exists(self, mock_discord_call):
        mock_discord_call.return_value = MockDiscordResponse(status_code=404)
        try:
            remove_discord_user(self.discord_user.external_id)
        except Exception as e:
            pass
        self.assertTrue(DiscordUser.objects.filter(
            external_id=self.discord_user.external_id).exists())

    @patch('django_discord_connector.tasks.DiscordRequest.get_discord_user')
    def test_update_discord_user_no_nickname(self, mock_discord_call):
        mock_discord_call.return_value = MockDiscordResponse(status_code=200, response={
            "nick": None,
            "user": {
                "discriminator": "#1337",
                "username": "username",
            }
        })
        update_discord_user(self.discord_user.external_id)

    @patch('django_discord_connector.tasks.update_remote_discord_user_nickname')
    def test_enforce_discord_nicknames(self, mock_task):
        from django_eveonline_connector.models import PrimaryEveCharacterAssociation, EveCharacter, EveCorporation, EveAlliance

        alliance = EveAlliance.objects.create(
            external_id=3,
            name="Alliance Name",
            ticker="ALLI"
        )

        corporation = EveCorporation.objects.create(
            external_id=2,
            name="Corporation Name",
            ticker="CORP",
            alliance=alliance
        )

        character = EveCharacter.objects.create(
            external_id=1,
            name="Character Name",
            corporation=corporation
        )

        PrimaryEveCharacterAssociation(
            user=self.user,
            character=character
        ).save()

        mock_task.return_value = None

        settings = DiscordClient.get_instance()
        settings.name_enforcement_schema = "[%alliance] [%corporation] [%username] - [%character]"
        settings.save()

        enforce_discord_nicknames()

        self.discord_user.refresh_from_db()
        self.assertEqual(
            "[ALLI] [CORP] [test] - [Character Name]", self.discord_user.nickname)
