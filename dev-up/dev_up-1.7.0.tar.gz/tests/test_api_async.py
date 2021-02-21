import asyncio
import os
from datetime import datetime

from aiounittest import AsyncTestCase

from dev_up import DevUpAPI, models


class TestDevUpAPIAsync(AsyncTestCase):
    _loop = None

    @property
    def loop(self):
        if self._loop is None:
            self._loop = asyncio.get_event_loop()
        return self._loop

    def setUp(self) -> None:
        TOKEN = os.environ['TOKEN']
        self.api = DevUpAPI(TOKEN, self.loop)

    def get_event_loop(self):
        return self.loop

    async def test_make_request_async(self):
        result = await self.api.make_request_async("profile.get", dict())
        self.assertIn('response', result, 'any')

    async def test_profile_get_async(self):
        profile = await self.api.profile.get_async()
        self.assertIsInstance(profile, models.ProfileGet)
        self.assertIsInstance(profile.response.req_datetime, datetime)
        self.assertIsInstance(profile.response.last_online_datetime, datetime)

    async def test_vk_get_stickers_async(self):
        stickers = await self.api.vk.get_stickers_async(1)
        self.assertIsInstance(stickers, models.VkGetStickers)

    async def test_vk_get_sticker_info_async(self):
        stickers = await self.api.vk.get_sticker_info_async(54983)
        self.assertIsInstance(stickers, models.VkGetStickerInfo)

    async def test_vk_get_apps_async(self):
        apps = await self.api.vk.get_apps_async(1)
        self.assertIsInstance(apps, models.VkGetApps)

    async def test_vk_get_groups_async(self):
        groups = await self.api.vk.get_groups_async(1)
        self.assertIsInstance(groups, models.VkGetGroups)

    async def test_utils_md5_generate_async(self):
        md5 = await self.api.utils.md5_generate_async("text")
        self.assertIsInstance(md5, models.UtilsMD5Generate)

    async def test_utils_get_server_time_async(self):
        server_time = await self.api.utils.get_server_time_async()
        self.assertIsInstance(server_time, models.UtilsGetServerTime)
        self.assertIsInstance(server_time.response.datetime, datetime)

    async def test_utils_create_short_link_async(self):
        short_link = await self.api.utils.create_short_link_async("https://vk.com/lordralinc")
        self.assertIsInstance(short_link, models.UtilsCreateShortLink)
        self.assertIsInstance(short_link.response.create_datetime, datetime)

    async def test_utils_notifications_links_async(self):
        short_link_not = await self.api.utils.notifications_links_async(
            code="/4c251",
            status=models.NotificationsLinksStatus.OFF
        )
        self.assertIsInstance(short_link_not, models.UtilsNotificationsLinks)

    async def test_get_web_info_async(self):
        urls = [
            "google.com",
            "vk.com",
            "87.240.190.78"
        ]
        for url in urls:
            info = await self.api.utils.get_web_info_async(url)
            self.assertIsInstance(info, models.UtilsGetWebInfo)