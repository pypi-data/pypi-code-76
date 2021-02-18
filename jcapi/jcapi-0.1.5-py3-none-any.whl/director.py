"""Handles communication with a Jiachang Director, and provides functions for getting details about items on the Director.
"""
import aiohttp
import async_timeout
import json
from .error_handling import checkResponseForError
import logging

_LOGGER = logging.getLogger(__name__)


class JcDirector:
    def __init__(
            self,
            ip,
            director_bearer_token,
            session_no_verify_ssl: aiohttp.ClientSession = None,
    ):
        """Creates a Jiachang Director object.

        Parameters:
            `ip` - The IP address of the Jiachang Director/Controller.
            "/home/status.php&hictoken=2802-1572318277-980006311-18755fdbf8-c525d56258"
            `director_bearer_token` - The bearer token used to authenticate with the Director. See `pyJiachang.account.JcAccount.getDirectorBearerToken` for how to get this.

            `session` - (Optional) Allows the use of an `aiohttp.ClientSession` object for all network requests. This session will not be closed by the library.
            If not provided, the library will open and close its own `ClientSession`s as needed.
        """
        self.base_url = ip
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self.session = session_no_verify_ssl
        self.token = director_bearer_token

    async def request(self, uri, params, async_variable=True):
        """Sends a POST request to the specified API URI. Used to send commands to the Director.
        Returns the Director's JSON response as a string.

        Parameters:
            `uri` - The API URI to send the request to. Do not include the IP address of the Director.

            `command` - The Jiachang command to send.

            `params` - The parameters of the command, provided as a dictionary.
        """
        url = self.base_url + uri + "?hictoken=" + self.token

        json_dict = params

        if self.session is None:
            async with aiohttp.ClientSession() as session:
                with async_timeout.timeout(10):
                    async with session.post(
                            url, data=json_dict
                    ) as resp:
                        # await checkResponseForError(await resp.text())
                        return await resp.text()
        else:
            with async_timeout.timeout(10):
                async with self.session.post(
                        url, data=json_dict
                ) as resp:
                    # await checkResponseForError(await resp.text())
                    return await resp.text()

    async def get_all_item_info(self):
        """Returns a JSON list of all the items on the Director.
        """
        # res = await self.request(uri="/home/status.php", params={"rs":"getDevListJson"})
        # print(res)
        return await self.request(uri="/home/status.php", params={"rs": "getDevListJson"})

    async def get_item_info(self, item_id):
        """Returns a JSON list of the details of the specified item.

        Parameters:
            `item_id` - The Jiachang item ID.
        """
        data = {
            "rs": "getAttr",
            "rsargs[]": item_id
        }
        return await self.request(uri="/devattr/devattr.php", params=data)

    async def get_item_variable_value(self, item_id, var_name, dev_type):
        """Returns the value of the specified variable for the specified item as a string.

        Parameters:
            `item_id` - The Jiachang item ID.

            `var_name` - The Jiachang variable name.
        """
        data = await self.get_item_info(item_id)

        if data:
            json_dictionary = json.loads(data)
            # if dev_type == "switch" or dev_type == "cl" or dev_type == "cl1":
            #     return json_dictionary["value"]
            if dev_type == "color":
                return json_dictionary["value"].get(var_name, 0)
            else:
                return json_dictionary["value"]
        else:
            raise ValueError(
                f"Empty response recieved from Director! The variable {var_name} doesn't seem to exist for item {item_id}."
            )
