import os
from datetime import datetime
from unittest import TestCase

from dev_up import DevUpAPI, models


class TestDevUpAPI(TestCase):

    def setUp(self) -> None:
        TOKEN = os.environ['TOKEN']
        self.api = DevUpAPI(TOKEN)

    def test_make_request(self):
        result = self.api.make_request("profile.get", dict())
        self.assertIn('response', result)

    def test_profile_get(self):
        profile = self.api.profile.get()
        self.assertIsInstance(profile, models.ProfileGet)
        self.assertIsInstance(profile.response.req_datetime, datetime)
        self.assertIsInstance(profile.response.last_online_datetime, datetime)

    def test_vk_get_stickers(self):
        stickers = self.api.vk.get_stickers(1)
        self.assertIsInstance(stickers, models.VkGetStickers)

    def test_vk_get_sticker_info(self):
        stickers = self.api.vk.get_sticker_info(54983)
        self.assertIsInstance(stickers, models.VkGetStickerInfo)

    def test_vk_get_apps(self):
        apps = self.api.vk.get_apps(1)
        self.assertIsInstance(apps, models.VkGetApps)

    def test_vk_get_groups(self):
        groups = self.api.vk.get_groups(1)
        self.assertIsInstance(groups, models.VkGetGroups)

    def test_utils_md5_generate(self):
        md5 = self.api.utils.md5_generate("text")
        self.assertIsInstance(md5, models.UtilsMD5Generate)

    def test_utils_get_server_time(self):
        server_time = self.api.utils.get_server_time()
        self.assertIsInstance(server_time, models.UtilsGetServerTime)
        self.assertIsInstance(server_time.response.datetime, datetime)

    def test_utils_create_short_link(self):
        short_link = self.api.utils.create_short_link("https://vk.com/lordralinc")
        self.assertIsInstance(short_link, models.UtilsCreateShortLink)
        self.assertIsInstance(short_link.response.create_datetime, datetime)

    def test_utils_notifications_links(self):
        short_link_not = self.api.utils.notifications_links(
            code="/4c251",
            status=models.NotificationsLinksStatus.OFF
        )
        self.assertIsInstance(short_link_not, models.UtilsNotificationsLinks)

    def test_get_web_info(self):
        urls = [
            "google.com",
            "vk.com",
            "87.240.190.78"
        ]
        for url in urls:
            info = self.api.utils.get_web_info(url)
            self.assertIsInstance(info, models.UtilsGetWebInfo)
