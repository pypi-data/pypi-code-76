import asyncio

from ratelimit import limits, sleep_and_retry

import aiohttp
from async_timeout import timeout

from . import exceptions

# pylint: disable=pointless-string-statement
""":copyright: (c) 2020 by Robert Hillis.
Not affiliated with Goal Zero. Credit for headers belongs to Goal Zero.
:license: Apache 2.0, see LICENSE for more details."""


HEADER = {
    "Content-Type": "application/json",
    "User-Agent": "YetiApp/1340 CFNetwork/1125.2 Darwin/19.4.0",
    "Connection": "keep-alive",
    "Accept": "application/json",
    "Accept-Language": "en-us",
    "Content-Length": "19",
    "Accept-Encoding": "gzip, deflate",
    "Cache-Control": "no-cache",
}
TIMEOUT = 10


class Yeti:
    """A class for handling connections with a Goal Zero Yeti."""

    def __init__(self, host, loop, session, **data):
        """Initialize the connection to Goal Zero Yeti instance."""
        self._loop = loop
        self._session = session
        self.control = {}
        self.data = {}
        self.endpoint = {}
        self.host = host
        self.payload = {}

    async def get_state(self):
        """Get states from Goal Zero Yeti instance."""
        self.control = "thingName"
        self.endpoint = "/state"
        await Yeti.send_get(self)

    async def post_state(self, payload):
        """Post payload to Goal Zero Yeti instance."""
        self.endpoint = "/state"
        self.payload = payload
        await Yeti.send_post(self)

    async def sysinfo(self):
        """Get system info from Goal Zero Yeti instance."""
        self.endpoint = "/sysinfo"
        self.control = "name"
        await Yeti.send_get(self)

    async def reset(self):
        """Reset Goal Zero Yeti instance."""
        self.endpoint = "/factory-reset"
        await Yeti.send_get(self)

    async def reboot(self):
        """Reboot Goal Zero Yeti instance."""
        self.endpoint = "/rpc/Sys.Reboot"
        await Yeti.send_get(self)

    async def get_loglevel(self):
        """Get log level Goal Zero Yeti instance."""
        self.endpoint = "/loglevel"
        self.control = "app"
        await Yeti.send_get(self)

    async def post_loglevel(self, payload):
        """Post log level Goal Zero Yeti instance."""
        self.endpoint = "/loglevel"
        self.payload = payload
        await Yeti.send_post(self)

    async def join(self, payload):
        """Join Goal Zero Yeti instance to Wifi network."""
        self.endpoint = "/join"
        self.payload = payload
        await Yeti.send_post(self)

    async def wifi(self):
        """Get available Wifi networks visible to Goal Zero Yeti instance."""
        self.endpoint = "/wifi"
        await Yeti.send_get(self)

    async def password_set(self, payload):
        """Set password to Zero Yeti instance."""
        self.payload = {"new_password": "" + payload + ""}
        self.endpoint = "/password-set"
        await Yeti.send_post(self)

    async def join_direct(self, payload):
        """Directly Join Goal Zero Yeti instance on its Wifi."""
        self.endpoint = "/join-direct"
        await Yeti.send_post(self)

    async def start_pair(self):
        """Pair with Goal Zero Yeti instance."""
        self.endpoint = "/start-pair"
        await Yeti.send_post(self)

    @sleep_and_retry
    @limits(calls=1, period=2)
    async def send_get(self):
        """Send get request."""
        try:
            async with timeout(TIMEOUT, loop=self._loop):
                response = await self._session.get(
                    "http://" + self.host + self.endpoint
                )
                self.data = await response.json()
                if self.control not in self.data.keys():
                    raise exceptions.InvalidHost()
                if self.data["socPercent"] > 100:
                    self.data["socPercent"] = 100
        except aiohttp.client_exceptions.ClientConnectorError:
            raise exceptions.ConnectError() from aiohttp.client_exceptions.ClientConnectorError
        except asyncio.exceptions.TimeoutError:
            raise exceptions.ConnectError() from asyncio.exceptions.TimeoutError
        except aiohttp.client_exceptions.ServerDisconnectedError:
            pass

    @sleep_and_retry
    @limits(calls=1, period=2)
    async def send_post(self):
        """Send post request."""
        try:
            async with timeout(TIMEOUT, loop=self._loop):
                request = await self._session.post(
                    "http://" + self.host + self.endpoint,
                    json=self.payload,
                    headers=HEADER,
                )
                self.data = await request.json()
                if self.data["socPercent"] > 100:
                    self.data["socPercent"] = 100
        except aiohttp.client_exceptions.ClientConnectorError:
            raise exceptions.ConnectError() from aiohttp.client_exceptions.ClientConnectorError
        except aiohttp.client_exceptions.ServerDisconnectedError:
            pass
