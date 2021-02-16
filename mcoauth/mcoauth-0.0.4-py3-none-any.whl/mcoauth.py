from aiohttp import *
import asyncio
import requests

class MCOauthFailed(Exception):
    """
    Class when something wrong happened with MCOauth and we can't be more specific about what happened.
    All module exceptions extend this exception.
    Catch with 
    ```
    except MCOauthFailed
    ```
    if you have MCOauthFailed imported like so
    ```
    from mcoauth import *
    ```
    if that is not the case, use
    ```
    except mcoauth.MCOauthFailed
    ```
    """
    pass
class InvalidToken(MCOauthFailed):
    """
    Exception raised when token is invalid or expired
    Catch with 
    ```
    except InvalidToken
    ```
    if you have InvalidToken imported like so
    ```
    from mcoauth import *
    ```
    if that is not the case, use
    ```
    except mcoauth.InvalidToken
    ```
    """
    pass
class MinecraftPlayer():
    """A Minecraft Player. Create from a token supplied. Fully async, but __init__ is not async"""
    async def handle_fail(self, message):
        """
        Internal function to handle a fail message.
        Do not use under normal circumstances.
        """
        if message == "Invalid or expired token":
            raise InvalidToken
        else:
            print("Hey, it's the developers. You've found a new fail message. Go to the GitHub repository and make a new Issue with the fail message and how to reproduce.")
    async def populate_self(self, token):
        """Internal Function to populate the self variable with username and uuid"""
        headers = {
         "token": str(token)
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get('https://mc-oauth.net/api/api?token') as resp:
                if resp.status == 200:
                    json = await response.json()
                    if json["status"] == "fail":
                        await self.handle_fail(json["message"])
                        return
                    self.uuid = json["uuid"]
                    self.username = json["username"]
                else:
                    json = await response.json()
                    if json["status"] == "fail":
                        await self.handle_fail(json["message"])
                        return
                    self.uuid = json["uuid"]
                    self.username = json["username"]
    def __init__(self, token):
        """Creates a new Minecraft User from a MCOauth token"""
        self.token = int(token)
        asyncio.run(self.populate_self(token))
    def __int__(self):
        return self.token
    def __index__(self):
        return self.__int__
