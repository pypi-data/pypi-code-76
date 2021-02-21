"""
This file contains the Extreme EXOS RESTCONF device asyncio Client.
"""

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

import httpx

# -----------------------------------------------------------------------------
# Exports
# -----------------------------------------------------------------------------

__all__ = ["Device"]


class Device(httpx.AsyncClient):
    """
    This Device class provides the asyncio RESTCONF client for Extreme EXOS.
    The device must be configured with web http or https service.

    References
    ----------
    https://api.extremenetworks.com/EXOS/ProgramInterfaces/RESTCONF/RESTCONF.html
    """

    DEFAULT_PROTO = "https"
    URL_RESTCONF = "/rest/restconf/data/"

    def __init__(self, host, username, password, proto=None, **kwargs):
        base_url = f"{proto or self.DEFAULT_PROTO}://{host}"
        kwargs.setdefault("verify", False)

        super().__init__(base_url=base_url, **kwargs)

        self.headers["Content-Type"] = "application/json"
        self.__auth = dict(username=username, password=password)

    async def login(self):
        """
        This coroutine is used to authenticate with the device to obtain a
        session token used for further command access.  Upon completiton the
        base URL will be shifted to use the URL_RESTCONF value.

        Raises
        ------
        httpx.HTTPError if request status is not OK.
        """
        res = await self.post("/auth/token/", json=self.__auth)
        res.raise_for_status()
        self.headers["X-Auth-Token"] = res.json()["token"]
        self.base_url = self.base_url.join(self.URL_RESTCONF)
