#! /usr/bin/env python3

import logging
import datetime

from . import constants


logger = logging.getLogger(__name__)
logger.setLevel(constants.LOG_LEVEL)

file_handler = logging.FileHandler(constants.TWITCH_OBJ_LOG)
formatter = logging.Formatter(constants.TWITCH_OBJ_FORM)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class EmptyValue():
    """Define empty values if Twitch returns 'Null'"""

    def _noGameId(self):
        """If game_id is not found return ID: 0"""

        empty = {'game_id': 0}
        self._data.update(empty)


class Merge():
    """Merges two objects and their data"""

    @staticmethod
    def _merge(merge_items, item, key):
        for merge_item in merge_items:
            if merge_item == item:
                ob = dict(item.__dict__[key])
                ob.update(dict(merge_item.__dict__[key]))
        return ob


class User():
    _keys = {
        'user_id': {
            'twitch': 'id',
            'pretty': 'ID'},
        'display_name': {
            'twitch': 'display_name',
            'pretty': 'Display Name'}}
    _key_source = 'user'

    def __init__(self, *ignore, raw):
        self._keys = dict(self._keys)
        if raw:
            self._data = self.__genData(raw)

    def __hash__(self):
        h = int(self._data['user_id'])
        return h

    def __eq__(self, other):
        if isinstance(other, User):
            return hash(other) == self.__hash__()
        else:
            return NotImplemented

    def __repr__(self):
        return f'{self.__class__.__name__}({self._data})'

    def __genData(self, raw):
        data = {}
        for k in self._keys:
            data[k] = raw[self._keys[k]['twitch']]
        return data

    def get(self, key):
        return self._data[key]

    def getKeys(self):
        # keys = tuple(self._keys)
        return self._keys

    def getUserId(self):
        return self.get('user_id')

    def getDispName(self):
        return self.get('display_name')

    def getKeySource(self):
        return self._key_source

    # def getPretty(self, keys):
    #     pretty = []
    #     for key in keys:
    #         if key in self._keys:
    #             pretty.append(self._keys[key]['pretty'])
    #     return pretty


class TwitchFollow(User):
    __follow_keys = {
        'user_id': {
            'twitch': 'to_id'},
        'name': {
            'twitch': 'to_login'},
        'display_name': {
            'twitch': 'to_name'},
        'followed_from': {
            'twitch': 'followed_at'}}
    _key_source = 'twitch_follow'

    def __init__(self, *ignore, raw=False, data=False):
        self._keys = self.__follow_keys
        if raw and not data:
            super().__init__(raw=raw)
        elif data and not raw:
            self._data = data

    def __hash__(self):
        h = int(self._data['user_id'])
        return h

    def __eq__(self, other):
        if isinstance(other, User):
            return other.getId() == self.__hash__()
        else:
            return NotImplemented

    def getId(self):
        return self.get('user_id')

    def getName(self):
        return self.get('name')

    def getFollowedFrom(self):
        return self.get('followed_from')


class Game(User):
    __game_keys = {
        'box_art_url': {
            'twitch': 'box_art_url',
            'pretty': 'Box Art URL'},
        'game_id': {
            'twitch': 'id',
            'pretty': 'Game ID'},
        'game': {
            'twitch': 'name',
            'pretty': 'Game'}}
    _key_source = 'game'

    def __init__(self, *ignore, raw=False, data=False):
        self._keys = self.__game_keys
        if raw and not data:
            super().__init__(raw=raw)
            if not self.getGameId():
                self._noGameId()
        elif data and not raw:
            self._data = data

        # else:
        #     self._data = {
        #         'box_art_url': 'Unknown',
        #         'game_id': '0',
        #         'game': 'Unknown'}

    def __hash__(self):
        h = int(self._data['game_id'])
        return h

    def __eq__(self, other):
        if isinstance(other, User):
            return other.getGameId() == self.__hash__()
        else:
            return NotImplemented

    def getBoxArtUrl(self):
        return self.get('box_art_url')

    def getGameId(self):
        return self.get('game_id')

    def getGame(self):
        return self.get('game')


class UserData(User):
    __offline_keys = {
        'name': {
            'twitch': 'login',
            'pretty': 'Name'},
        'type': {
            'twitch': 'type',
            'pretty': 'Type'},
        'partner': {
            'twitch': 'broadcaster_type',
            'pretty': 'Twitch Status'},
        'description': {
            'twitch': 'description',
            'pretty': 'Description'},
        'icon_url': {
            'twitch': 'profile_image_url',
            'pretty': 'Icon URL'},
        'offline_image': {
            'twitch': 'offline_image_url',
            'pretty': 'Offline Image'},
        'view_count': {
            'twitch': 'view_count',
            'pretty': 'View Count'}}
    _key_source = 'userdata'

    def __init__(self, *ignore, raw=False, data=False):
        self._keys = dict(self._keys)
        if raw and not data:
            # self._keys = dict(self._keys())
            self._keys.update(self.__offline_keys)
            super().__init__(raw=raw)
        elif data and not raw:
            self._data = data
        else:
            # self._keys = dict(self._keys())
            self._keys.update(self.__offline_keys)
            # m = 'UserData __init__() requires either "raw" or "data" keyword'
            # raise TypeError(m)

    def getName(self):
        return self.get('name')

    def getType(self):
        return self.get('type')

    def getPartner(self):
        return self.get('partner')

    def getDesc(self):
        return self.get('description')

    def getIconUrl(self):
        return self.get('icon_url')

    def getOfflineImage(self):
        return self.get('offline_image')

    def getViewCount(self):
        return self.get('view_count')


class Vod(User):
    __vod_keys = {
        'vod_id': {
            'twitch': 'id',
            'pretty': 'Vod ID'},
        'user_id': {
            'twitch': 'user_id',
            'pretty': 'User ID'},
        'display_name': {
            'twitch': 'user_name',
            'pretty': 'Display Name'},
        'vod_title': {
            'twitch': 'title',
            'pretty': 'Vod Title'},
        'vod_description': {
            'twitch': 'description',
            'pretty': 'Vod Description'},
        'created_at': {
            'twitch': 'created_at',
            'pretty': 'Created At'},
        'published_at': {
            'twitch': 'published_at',
            'pretty': 'Published At'},
        'vod_url': {
            'twitch': 'url',
            'pretty': 'Vod URL'},
        'thumbnail_url': {
            'twitch': 'thumbnail_url',
            'pretty': 'Thumbnail URL'},
        'viewable': {
            'twitch': 'viewable',
            'pretty': 'Viewable'},
        'vod_view_count': {
            'twitch': 'view_count',
            'pretty': 'Vod View Count'},
        'language': {
            'twitch': 'language',
            'pretty': 'Language'},
        'vod_type': {
            'twitch': 'type',
            'pretty': 'Vod Type'},
        'duration': {
            'twitch': 'duration',
            'pretty': 'Duration'}}
    _key_source = 'vod'

    def __init__(self, *ignore, raw):
        self._keys = dict(self._keys)
        self._keys.update(self.__vod_keys)
        if raw:
            super().__init__(raw=raw)

    def getVodId(self):
        return self.get('vod_id')

    def getTitle(self):
        return self.get('vod_title')

    def getVideoDesc(self):
        return self.get('vod_description')

    def getCreatedAt(self):
        return self.get('created_at')

    def getPublishedAt(self):
        return self.get('published_at')

    def getVodUrl(self):
        return self.get('vod_url')

    def getThumbUrl(self):
        return self.get('thumbnail_url')

    def getViewable(self):
        return self.get('viewable')

    def getViewCount(self):
        return self.get('vod_view_count')

    def getLanguage(self):
        return self.get('language')

    def getType(self):
        return self.get('type')

    def getDuration(self):
        return self.get('duration')


class VodFullData(UserData, Vod):
    pass


class VodUser(VodFullData, Vod, Merge):
    def __init__(self, db, stream):
        self._keys = dict(self._keys)
        if db and stream:
            self._data = self._merge(db, stream, '_data')
        else:
            super().__init__(data=[])


class Stream(User, EmptyValue):
    __streaming_keys = {
        'user_id': {
            'twitch': 'user_id',
            'pretty': 'User ID'},
        'display_name': {
            'twitch': 'user_name',
            'pretty': 'Display Name'},
        'stream_id': {
            'twitch': 'id',
            'pretty': 'Stream ID'},
        'game_id': {
            'twitch': 'game_id',
            'pretty': 'Game ID'},
        'title': {
            'twitch': 'title',
            'pretty': 'Title'},
        'viewers': {
            'twitch': 'viewer_count',
            'pretty': 'Viewers'},
        'started_at': {
            'twitch': 'started_at',
            'pretty': 'Started At'},
        'thumbnail_url': {
            'twitch': 'thumbnail_url',
            'pretty': 'Thumbnail URL'},
        'tag_ids': {
            'twitch': 'tag_ids',
            'pretty': 'Tag IDs'}}
    _key_source = 'stream'

    def __init__(self, *ignore, raw):
        # self._keys = dict(self._keys)
        self._keys = dict(self._keys)
        self._keys.update(self.__streaming_keys)
        if raw:
            super().__init__(raw=raw)
            self.__insertTime()
            if not self.getGameId():
                self._noGameId()
        else:
            self._keys.update({'time': {'twitch': 'time', 'pretty': 'Time'}})

        # if not self.getGameId():
        #     empty = {'game_id': 0}
        #     self._data.update(empty)

    def __insertTime(self):
        started = self.getStarted()
        time_format = '%Y-%m-%dT%H:%M:%SZ'
        started_stamp = datetime.datetime.strptime(started, time_format)
        now = datetime.datetime.utcnow()
        delta = now - started_stamp
        time = str(datetime.timedelta(seconds=delta.seconds))
        self._data['time'] = time

    def getStreamId(self):
        return self.get('stream_id')

    def getGameId(self):
        return self.get('game_id')

    def getTitle(self):
        return self.get('title')

    def getViewers(self):
        return self.get('viewers')

    def getStarted(self):
        return self.get('started_at')

    def getThumbUrl(self):
        return self.get('thumbnail_url')

    def getTagIds(self):
        return self.get('tag_ids')

    def getTime(self):
        return self.get('time')


class CombineUserStream(UserData, Stream):
    pass


class StreamingUser(CombineUserStream, Stream, Merge):
    def __init__(self, db, stream):
        self._keys = dict(self._keys)
        if db and stream:
            self._data = self._merge(db, stream, '_data')
        else:
            super().__init__(data=[])

    # def get(self, key):
    #     def tryValue(key, i):
    #         try:
    #             value = self.__sources[i].get(key)
    #         except KeyError:
    #             return tryValue(key, i+1)
    #         return value
    #     return tryValue(key, 0)


class StreamingUserGame(StreamingUser, Game):
    def __init__(self, games, stream_user):
        self._keys = dict(self._keys)
        if games and stream_user:
            self._data = self._merge(games, stream_user, '_data')
        else:
            super().__init__(data=[])

    def __hash__(self):
        h = int(self._data['user_id'])
        return h

    def __eq__(self, other):
        if isinstance(other, StreamingUserGame):
            return hash(other) == self.__hash__()
        else:
            return NotImplemented

    @staticmethod
    def _merge(merge_items, item, key):
        for merge_item in merge_items:
            if hash(merge_item) == int(item.getGameId()):
                ob = dict(item.__dict__[key])
                ob.update(dict(merge_item.__dict__[key]))
        return ob
