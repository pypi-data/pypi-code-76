
import json
from aiohttp import ClientSession, BasicAuth, ClientError

SESSION_ID_HEADER_NAME = 'X-Transmission-Session-Id'

class TransmissionError(Exception):
    pass

class Transmission:

    def __init__(self, url, username = None, password = None):
        self._url = url
        self._username = username
        self._password = password
        self._session_id = ''


    async def torrent_list(self):
        data = await self._call('torrent-get', {
            "fields": [ "id", "name", "totalSize", "percentDone", "rateDownload", "sizeWhenDone", "eta", "rateUpload", "peersConnected" ],
        })
        return data['arguments']['torrents']

    async def session_stats(self):
        data = await self._call('session-stats')
        return data['arguments']

    async def _call(self, method: str, arguments: dict = {}):

        return await self._request({
            "arguments": arguments,
            "method": method,
        })

    async def _request(self, data: dict):

        headers = {
            SESSION_ID_HEADER_NAME: self._session_id,
        }

        auth = BasicAuth(self._username, self._password) if (self._username and self._password) else None

        try:

            async with ClientSession() as session:
                async with session.post(self._url, data = json.dumps(data), headers = headers, auth = auth) as response:

                    if response.status == 409 and self._session_id == '':
                        self._session_id = response.headers[SESSION_ID_HEADER_NAME]
                        return await self._request(data)

                    if response.status != 200:
                        raise TransmissionError(await response.text())

                    return await response.json()

        except ClientError as e:
            raise TransmissionError(str(e))
