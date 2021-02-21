"""
This file contains the Extreme EXOS JSON-RPC device asyncio Client.
"""

# -----------------------------------------------------------------------------
# System Imports
# -----------------------------------------------------------------------------

from typing import List, Union, Optional

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

import httpx

# -----------------------------------------------------------------------------
# Exports
# -----------------------------------------------------------------------------

__all__ = ["Device"]


# -----------------------------------------------------------------------------
#
#                                 CODE BEGINS
#
# -----------------------------------------------------------------------------


class Device(httpx.AsyncClient):
    """
    The Device class implements a JSON-RPC asyncio client for Extreme EXOS.  In
    order to connect to the target device the web http or https service must be
    enabled.
    """

    DEFAULT_PROTO = "https"

    def __init__(self, host, username, password, proto=None, **kwargs):
        """
        Create a new device instance.

        As a subclass of httpx.AsyncClient any constructor parameters are
        supported.  If using https the SSL verification is disabled by default.

        Parameters
        ----------
        host: str
            The hostname or IP address of the target device

        username: str
            The login user-name

        password: str
            The login password

        Other Parameters
        ----------------
        proto: str
            OneOf ['http', 'https']
        """
        base_url = f"{proto or self.DEFAULT_PROTO}://{host}"

        kwargs.setdefault("verify", False)
        kwargs.setdefault("auth", (username, password))

        super().__init__(base_url=base_url, **kwargs)
        self.headers["Content-Type"] = "application/json"

        self._req_id = 0

    def jsonrpc(self, commands: str):
        """
        This function generates the JSON-RPC payload required by EXOS.

        Parameters
        ----------
        commands: List[str]

        Returns
        -------
        dict - payload to be used to post the JSON-RPC reuqest.
        """
        self._req_id += 1

        return {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": [commands],
            "id": self._req_id,
        }

    async def cli(
        self, commands: Union[str, List[str]], text: Optional[bool] = False
    ) -> List:
        """
        This coroutine is used to execute one or more CLI commands and return
        the results in either dict or text format.

        Parameters
        ----------
        commands: str or List[str]
            As a str, this value is generally just a single command such as
            "show switch".  The str value can also be a semi-colon separated
            list of commands such as "show switch;show ports".

            As a list of strings, each list item is a single command, for
            example ['show switch', 'show ports'].

        text: bool
            When True return the results as the CLI text output.
            When False (default) results are the dict payload.

        Returns
        -------
        List of command results, even if only one command provided.

        Raises
        ------
        httpx.HTTPError when response status code is not OK.
        """
        if isinstance(commands, list):
            commands = ";".join(commands)

        command_count = commands.count(";") + 1

        res = await self.post("/jsonrpc", json=self.jsonrpc(commands))
        res.raise_for_status()
        result = res.json()["result"]

        # The the Caller wants the text output, then return the list of CLI
        # output items.

        if text is True:
            if command_count == 1:
                return [result[0]["CLIoutput"]]

            cli_text = list()
            for cmd_i in range(command_count):
                cli_text.append(result[cmd_i].pop(0)["CLIoutput"])

            return cli_text

        # otherwise the Caller wants the dict payload results

        if command_count == 1:
            return result[1:]

        res_data = list()
        for cmd_i in range(command_count):
            res_data.append(result[cmd_i][1:])

        return res_data

    async def get_config(self) -> str:
        """
        This coroutine returns the configuration in text format.
        """
        res = await self.cli("show configuration", text=True)
        return res[0]

    # -------------------------------------------------------------------------
    #
    #                           AsyncClient Overrides
    #
    # -------------------------------------------------------------------------

    async def request(self, *vargs, **kwargs) -> httpx.Response:
        res = await super().request(*vargs, **kwargs)

        # store the session as a cookie-header so that the device does not need
        # to use the auth for parameter for re-authentication each time.

        if not res.is_error:
            self.headers["Cookie"] = f"session={self.cookies['session']}"

        return res
