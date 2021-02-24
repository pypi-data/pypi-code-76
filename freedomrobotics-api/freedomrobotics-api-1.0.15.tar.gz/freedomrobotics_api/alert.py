import json
import time
from .helpers import to_unix_time


class Alert(object):
    """An alert within the Freedom Robotics API. Not intended to be manually instantiated by the user of the API.

    Args:
        _id (str): Alert ID.
        _data (`dict`): Alert data.
    """

    def __init__(self, _id, _data):
        self._id = _id
        self._data = _data

    def __repr__(self):
        return "<Alert: {} {}>".format(self._id, self._data.get("name", ""))

    def __eq__(self, obj):
        return isinstance(obj, Alert) and obj._id == self._id

    @property
    def attributes(self):
        return self._data.get("attributes")

    @property
    def action(self):
        return self._data.get("action")

    @property
    def account_name(self):
        return self._data.get("account_name")

    @property
    def description(self):
        return self._data.get("description")

    @property
    def device_name(self):
        return self._data.get("device_name")

    @property
    def level(self):
        return self._data.get("level")

    @property
    def name(self):
        return self._data.get("name")

    @property
    def replay_url(self):
        return self._data.get("replay_url")

    @property
    def type(self):
        return self._data.get("type")

    @property
    def utc_time(self):
        return to_unix_time(self._data.get(utc_time))
