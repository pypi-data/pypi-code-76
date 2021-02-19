#! /usr/bin/env python3


import os
import re
import logging
import webbrowser
from pathlib import Path

from . import constants
from . fileoperator import FileOperator


logger = logging.getLogger(__name__)
logger.setLevel(constants.LOG_LEVEL)
# logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(constants.TOOLS_LOG)
formatter = logging.Formatter(constants.TOOLS_FORM)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class TwitchInfo():
    """API key information"""

    __keys = {
        'name': {'twitch': 'login'},
        'user_id': {'twitch': 'user_id'},
        'expire': {'twitch': 'expires_in'}}

    def __init__(self, fo):
        self.__fo = fo
        self.__data = self.__fo.loadFile() or {}
        logger.debug('[INIT] TwitchInfo()')

    def __saveInfo(self):
        """Save data to twitch.json"""

        self.__fo.saveFile(self.__data)

    def setToken(self, token):
        """Set Twitch token"""

        self.__data['token'] = token
        logger.debug(f'[SET_TOKEN] Twitch Validation: Token {self.__data}')
        self.__saveInfo()

    def setValidate(self, data):
        """Set API key validation data"""

        self.__data['name'] = data[self.__keys['name']['twitch']]
        self.__data['user_id'] = data[self.__keys['user_id']['twitch']]
        self.__data['expire'] = data[self.__keys['expire']['twitch']]
        logger.debug(f'[SET_VALIDATE] Twitch Validation: Data {self.__data}')
        self.__saveInfo()

    def getData(self):
        """Return twitch.json"""

        logger.debug('[DATA] data return')
        return self.__data

    def getToken(self):
        """Return token from twitch.json"""

        logger.debug('[TOKEN] info return')
        return self.__data.get('token')

    def getId(self):
        """Return user id from twitch.json"""

        logger.debug('[ID] id return')
        return self.__data.get('user_id')


def oauth(funcIntpu):
    """Returns OAuth key"""

    twitch = constants.TWITCH
    base = constants.BASES[os.name]
    p = base / Path(twitch)

    fo = FileOperator(str(p))

    def __generateOAuth():
        """Open URL for Twitch OAuth key generation"""

        url = (
            'https://id.twitch.tv/oauth2/authorize'
            '?client_id=m3ggy4wqrvs4sfhv996glushskv1fi'
            '&redirect_uri=http://localhost'
            '&response_type=token')
        logger.debug(f'[OAUTH] open URL: "{url}"')
        webbrowser.open_new_tab(url)

    def getKey():
        """Return OAuth if found in file, open URL if not"""

        # oauth = fo.loadFile(singleLayer=True)
        twitch_info = TwitchInfo(fo)
        # if twitch and twitch['token']:
        #     return twitch['token']
        if twitch_info.getToken():
            logger.debug('[KEY] token found')
            return twitch_info
            # return twitch_info.getToken()
        else:
            logger.debug('[KEY] token not found')
            __generateOAuth()
            print('Paste resulting URL after doing Twitch login')
            url = funcIntpu()

            # r = re.compile(
            #     r'^(http://localhost/)'
            #     r'(\#access_token=([a-z0-9]+))'
            #     r'(&scope=&token_type=bearer)$')
            r = tokenReCompile()
            match = r.match(url)

            if match:
                logger.debug('[KEY] token match found from URL')
                oauth = match.groups()[2]
                # fo.saveFile([oauth])
                # twitch.update({'token': oauth})
                # fo.saveFile(twitch)
                # return oauth
                twitch_info.setToken(oauth)
                return twitch_info
            else:
                logger.debug('[KEY] token not found from URL')
                raise ValueError('Given link was not recognized')

    return getKey()


def tokenReCompile():
    r = re.compile(
        r'^(http://localhost/)'
        r'(\#access_token=([a-z0-9]+))'
        r'(&scope=&token_type=bearer)$')
    return r
