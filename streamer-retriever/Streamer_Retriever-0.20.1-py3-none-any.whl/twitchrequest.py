#! /usr/bin/env python3


import re
import json
import logging
from urllib import request
from urllib.error import URLError

from . import constants
from . twitchobjs import (
    TwitchFollow,
    Game,
    UserData,
    Vod,
    Stream)


logger = logging.getLogger(__name__)
logger.setLevel(constants.LOG_LEVEL)
# logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(constants.TWITCH_API_LOG)
formatter = logging.Formatter(constants.TWITCH_API_FORM)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class TwitchAPI():
    """Performs API calls to Twitch"""

    def __init__(self, oauth):
        self.__headers = {
            'Client-ID': 'm3ggy4wqrvs4sfhv996glushskv1fi',
            'Authorization': 'Bearer ' + oauth}
        self.__oauth = oauth

    def _makeUrl(self, names):
        """Returns values as request URL if values match regex"""

        first = self._twitch_dict['first']
        conf = self._twitch_dict['cont']
        names_ext = first + conf.join(names)
        in_url = self._twitch_dict['url'] + names_ext

        reg = self._twitch_dict['reg']
        r = re.compile(reg)
        match = r.match(in_url)

        if match:
            url = match.group()
            return url

    def request(self, url):
        """Perform Twitch request call"""

        # redundancy regex for URL
        r = re.compile(r'(https?://)([a-z]{1,3}\.)?(twitch.tv/)(.*)')
        reg_match = r.match(url)
        if not reg_match:
            logger.warning('[REQUEST] Twitch request received unexpected URL')
            raise ValueError('Twitch request received unexpected URL')

        try:
            h = request.Request(url, headers=self.__headers)
            u = request.urlopen(h)
        except URLError as e:
            logger.warning(f'Error using TwitchAPI: {e}')
            print("Error using Twitch API: ", e)
            return None

        j = json.loads(u.read().decode('utf-8'))
        logger.debug(f'[REQUEST] Headers: {self.__headers}')
        logger.debug(f'[REQUEST] URL: {url}')
        logger.debug(f'[REQUEST] Answer: {j}')
        return j


class TwitchValidate(TwitchAPI):
    """Give validation values for TwitchAPI()"""

    __url = 'https://id.twitch.tv/oauth2/validate'

    def __init__(self, oauth):
        logger.debug('[VALIDATE] get key validation')
        super().__init__(oauth)
        self.__data = self.request(self.__url)

    def get(self):
        """Return validation answer"""

        return self.__data


class TwitchLoadFollow(TwitchAPI):
    """Give check following values for TwitchAPI()"""

    _twitch_dict = {
        'url': 'https://api.twitch.tv/helix/users/follows',
        'first': '?from_id=',
        'cont': '',
        'reg': (
            r'(https://api.twitch.tv/helix/users/follows)'
            r'(\?from_id=[0-9]*$)')}

    def __init__(self, oauth, id_):
        logger.debug('[FOLLOWS] load follows from user')
        super().__init__(oauth)
        url = self._makeUrl(id_)
        self.__data = self.request(url)

    def get(self):
        """Return user following answer"""

        twitch_follows = tuple(
            TwitchFollow(raw=r) for r in self.__data['data'])
        return twitch_follows


class TwitchGameData(TwitchAPI):
    """Give game data values for TwitchAPI()"""

    _twitch_dict = {
        'url': 'https://api.twitch.tv/helix/games',
        'first': '?id=',
        'cont': '&id=',
        'reg': (
            r'^(https://api.twitch.tv/helix/games)'
            r'(\?id=[0-9]+)'
            r'(&id=[0-9]+)*$')}

    def __init__(self, oauth, ids):
        logger.debug('[GAME] get game data')
        super().__init__(oauth)
        url = self._makeUrl(ids)
        self.__data = self.request(url)

    def get(self):
        """Return game data answer"""

        games = tuple(Game(raw=r) for r in self.__data['data'])
        return games


class TwitchVod(TwitchAPI):
    """Give vod values for TwitchAPI()"""

    _twitch_dict = {
        'url': 'https://api.twitch.tv/helix/videos',
        'first': '?user_id=',
        'cont': '',
        'reg': (
            r'^(https://api.twitch.tv/helix/videos)'
            r'(\?user_id=[0-9]+)$')}

    def __init__(self, oauth, ids):
        logger.debug('[VOD] get vods')
        super().__init__(oauth)
        url = self._makeUrl(ids)
        self.__data = self.request(url) or {}

    def get(self):
        """Return vods for users answer"""

        vods = tuple(Vod(raw=r) for r in self.__data.get('data') or {})
        return vods


class TwitchStream(TwitchAPI):
    """Give stream values for TwitchAPI()"""

    _twitch_dict = {
        'url': 'https://api.twitch.tv/helix/streams',
        'first': '?user_login=',
        'cont': '&user_login=',
        'reg': (
            r'^(https://api.twitch.tv/helix/streams)'
            r'(\?user_login=[a-z0-9_]+)'
            r'(&user_login=[a-z0-9_]+)*$')}

    def __init__(self, oauth, names):
        logger.debug('[STREAM] get streaming')
        super().__init__(oauth)
        url = self._makeUrl(names)
        self.__data = self.request(url) or {}

    def get(self):
        """Return users streaming answer"""

        streams = tuple(Stream(raw=r) for r in self.__data.get('data') or {})
        return streams


class TwitchUserData(TwitchAPI):
    """Give user data values for TwitchAPI()"""

    _twitch_dict = {
        'url': 'https://api.twitch.tv/helix/users',
        'first': '?login=',
        'cont': '&login=',
        'reg': (
            r'^(https://api.twitch.tv/helix/users)'
            r'(\?login=[a-z0-9_]+)'
            r'(&login=[a-z0-9_]+)*$')}

    def __init__(self, oauth, names):
        logger.debug('[USER] get user data')
        super().__init__(oauth)
        url = self._makeUrl(names)
        self.__data = self.request(url)

    def get(self):
        """Return user data answer"""

        users = list(UserData(raw=r) for r in self.__data['data'])
        return users
