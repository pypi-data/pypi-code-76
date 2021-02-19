#! /usr/bin/env python3


import os
import re
import logging

from . import constants
from . twitchrequest import (
    TwitchValidate,
    TwitchLoadFollow,
    TwitchGameData,
    TwitchVod,
    TwitchStream,
    TwitchUserData)
from . twitchobjs import (
    Game,
    UserData,
    Vod,
    VodUser,
    Stream,
    StreamingUser,
    StreamingUserGame)
from . fileoperator import FileOperator


logger = logging.getLogger(__name__)
logger.setLevel(constants.LOG_LEVEL)

file_handler = logging.FileHandler(constants.STREAM_LOG)
formatter = logging.Formatter(constants.STREAM_FORM)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class Key():
    def __init__(self, index, key):
        self.__data = key
        self.__name = index

    def __eq__(self, other):
        if isinstance(other, Key):
            return other.getName() == self.getName()
        elif isinstance(other, str):
            return other == self.getName()
        else:
            return NotImplemented

    def __repr__(self):
        return f'{self.__class__.__name__}({{{self.__name}: {self.__data}}})'

    def getName(self):
        return self.__name

    def getDispName(self):
        return self.__data['pretty']


class StreamerRetriever():
    __base = constants.BASES[os.name]

    def __init__(self, info):
        # self.__oauth = info.getToken()
        self.__info = info
        self.__loadFiles()
        self.__upDb()

        u = UserData()
        s = Stream(raw=False)
        g = Game(raw=False)
        v = Vod(raw=False)
        sources = [u, s, g, v]
        self.__keys = {}
        for source in sources:
            self.__keys[source.getKeySource()] = dict(source.getKeys())

    def __loadFiles(self):
        b = self.__base
        self.__follows_fo = FileOperator(b + constants.FOLLOWS)
        self.__follows = self.__follows_fo.loadFile(singleLayer=True)

        self.__game_cache_fo = FileOperator(b + constants.GAME_CACHE)
        game_cache = self.__game_cache_fo.loadFile() or []
        self.__game_cache = list(Game(data=g) for g in game_cache)
        self.__cacheEmptyGame()

        # games = tuple(Game(raw=r) for r in self.__data['data'])

        self.__db_fo = FileOperator(b + constants.DB)
        dbs = self.__db_fo.loadFile()
        self.__users = tuple(UserData(data=db) for db in dbs)

    def __cacheGames(self, items):
        game_ids = set((i.getGameId() for i in items))
        cache_ids = set((c.getGameId() for c in self.__game_cache))
        new_ids = game_ids - cache_ids

        # apparently some games come as empty values
        # update = set(new if new else '0' for new in new_ids)
        update = set(new for new in new_ids if new)

        if update and update is not set():
            twitch_games = TwitchGameData(self.__info.getToken(), update)
            update_games = twitch_games.get()
            self.__game_cache.extend(update_games)
            self.__saveGameCache()

    def __cacheEmptyGame(self):
        for game in self.__game_cache:
            if hash(game) == 0:
                break
        else:
            empty = {
                'box_art_url': 'Unknown',
                'game_id': '0',
                'game': 'Unknown'}
            empty_game = Game(data=empty)
            self.__game_cache.append(empty_game)
            self.__saveGameCache()

    def __stream(self):
        if self.__follows:
            twitch_streaming = TwitchStream(
                self.__info.getToken(), self.__follows)
            streaming = twitch_streaming.get()
        else:
            streaming = []
        self.__cacheGames(streaming)
        return streaming

    def __getStreaming(self):
        stream = self.__stream()
        streaming_user = tuple(StreamingUser(self.__users, x) for x in stream)
        streaming_data = tuple(
            StreamingUserGame(self.__game_cache, y) for y in streaming_user)
        return streaming_data

    def __updateUsers(self):
        twitch_user_data = TwitchUserData(
            self.__info.getToken(), self.__follows)
        user_data = twitch_user_data.get()

        sorted_data = []
        for follow in self.__follows:
            for user in user_data:
                if user.getName() == follow:
                    sorted_data.append(user)

        self.__users = sorted_data

    def getFiles(self):
        files = {
            'follows': self.__follows_fo,
            'db': self.__db_fo,
            'game_cache': self.__game_cache_fo}
        return files

    def __saveGameCache(self):
        u = []
        for game in self.__game_cache:
            u.append(game.__dict__['_data'])
        self.__game_cache_fo.saveFile(u)

    def __saveDb(self):
        u = []
        for user in self.__users:
            u.append(user.__dict__['_data'])
        self.__db_fo.saveFile(u)

    # def __addRemoveDb(self):
    #     logger.info(
    #         f'Update DB removed: {set(db_follows) - set(self.__follows)}')
    #     logger.info(
    #         f'Update DB added: {set(self.__follows) - set(db_follows)}')
    #     new = set(self.__follows)
    #     old = set(db_follows)
    #     if new - old == set():
    #         self.__dbSorting()
    #     # elif new - old != new:
    #     #     self.__dbSorting()
    #     #     self.__updateUsers()
    #     else:
    #         self.__updateUsers()
    #     self.__saveDb()

    def __upDb(self):
        db_follows = []
        for f in self.__users:
            name = f.getName()
            db_follows.append(name)

        if set(db_follows) != set(self.__follows):
            logger.info(
                f'Update DB removed: {set(db_follows) - set(self.__follows)}')
            logger.info(
                f'Update DB added: {set(self.__follows) - set(db_follows)}')
            new = set(self.__follows)
            old = set(db_follows)
            if new - old == set():
                self.__dbSorting()
            # elif new - old != new:
            #     self.__dbSorting()
            #     self.__updateUsers()
            else:
                self.__updateUsers()
            self.__saveDb()
        elif db_follows != self.__follows:
            self.__dbSorting()

    def __dbSorting(self):
        db_sorted = []
        for f in self.__follows:
            for u in self.__users:
                if u.getName() == f:
                    db_sorted.append(u)
                    break
        self.__users = db_sorted
        self.__saveDb()
        logger.info(
            f'Update DB sorting: {tuple(e.getName() for e in db_sorted)}')

    def __saveFollows(self):
        self.__follows_fo.saveFile(self.__follows)

    def __cacheGameId(self, game_id):
        if game_id in self.__game_cache:
            pass

    def updateValidate(self):
        twitchValidate = TwitchValidate(self.__info.getToken())
        validation = twitchValidate.get()
        self.__info.setValidate(validation)

    def getValidate(self):
        return self.__info

    def getTwitchFollows(self):
        id_ = self.__info.getId()
        if not id_:
            self.updateValidate()
            id_ = self.__info.getId()
        twitch_load_follow = TwitchLoadFollow(self.__info.getToken(), id_)
        twitch_follows = twitch_load_follow.get()
        # follows = tuple(twitch.getName() for twitch in twitch_follows)
        # return follows
        return twitch_follows

    def updateDb(self, follows):
        self.__follows = follows
        self.__saveFollows()
        self.__upDb()

    def getDb(self):
        return self.__users

    def getPretty(self, keys):
        pretty = []
        for key in keys:
            for source in self.__keys:
                if key in self.__keys[source]:
                    pretty.append(self.__keys[key]['pretty'])
                else:
                    pretty.append(key)
        return pretty

    def getKeys(self, source=None):
        keys = {}
        if not source:
            for s in self.__keys:
                keys.update(self.__keys[s])
            return keys
        else:
            for s in source:
                keys.update(self.__keys[s])
            return keys

    def getKeyObjs(self, source=None):
        keys = self.getKeys(source)
        key_objs = list(Key(key, keys[key]) for key in keys)
        return key_objs

    def getOnline(self):
        return self.__getStreaming()

    def getVod(self, user_id):
        twitch_vods = TwitchVod(self.__info.getToken(), user_id)
        vods = twitch_vods.get()
        vod_user = tuple(VodUser(self.__users, x) for x in vods)
        return vod_user


if __name__ == '__main__':
    def oauth():
        import webbrowser

        base = constants.BASES[os.name]
        f = constants.TWITCH
        p = base + f

        fo = FileOperator(p)

        def __generateOAuth():
            url = (
                'https://id.twitch.tv/oauth2/authorize'
                '?client_id=m3ggy4wqrvs4sfhv996glushskv1fi'
                '&redirect_uri=http://localhost'
                '&response_type=token')
            webbrowser.open(url)

        def getKey():
            oauth = fo.loadFile(singleLayer=True)
            if oauth:
                return oauth[0]
            else:
                __generateOAuth()
                print('Paste resulting URL after doing Twitch login')
                url = input()

                r = re.compile(
                    r'^(http://localhost/)'
                    r'(\#access_token=([a-z0-9]+))'
                    r'(&scope=&token_type=bearer)$')
                match = r.match(url)

                if match:
                    oauth = match.groups()[2]
                    return oauth

        return getKey()

    def testingStreamerRetriever():
        pass
        # print(s.getDb())

        # print()
        # print(s.getOnline())

        # print()
        # print(StreamingUser({}, {}).getKeys())

        # print()
        # print(Stream(raw='').getKeys())

        # print()
        # users = []
        # for i, user in enumerate(s.getDb()):
        #     users.append(user)
        #     print(f'#{i+1} ' + user.getDispName())

        # user_in = int(input('#')) - 1
        # user_id = users[user_in].getUserId()
        # print(s.getVod(user_id))

    def testing():
        token = oauth()
        names = ['esl_csgo', 'esamarathon', 'gamesdonequick']

        twitch_user_data = TwitchUserData(token, names)
        user_data = twitch_user_data.get()
        for user in user_data:
            print(hash(user))
            print(user)
            print()

        twitch_streaming = TwitchStream(token, names)
        streaming = twitch_streaming.get()
        for stream in streaming:
            print(hash(stream))
            print(stream)
            print()

        # stream_users = tuple(StreamingUser(user_data, x) for x in streaming)
        # for s in stream_users:
        #     print(hash(s))
        #     print(s)
        #     print()

    def testUpdateDb():
        token = oauth()
        s = StreamerRetriever(token)
        follows = ['esamarathon', 'esl_csgo']
        s.updateDb(follows)

    token = oauth()
    # s = StreamerRetriever(token)
    # online = s.getOnline()
    # for o in online:
    #     # print(o)
    #     # print(o.__dict__)
    #     # print(o.getName() + ' - ' + o.getGame())
    #     pass

    def validate():
        twitch_validate = TwitchValidate(token)
        print(twitch_validate)

    # testing()
    # testingStreamerRetriever()
    # testUpdateDb()
