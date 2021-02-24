import time

from .api_handler import default_api


class Entity(object):
    """Base entity abstraction with common methods to update and push data the the API
    """

    def __init__(self, _id, _data=None, api=None, update_threshold=30):
        self._id = _id
        self._data = _data
        self._last_updated = None
        self._update_threshold = update_threshold
        if api is None:
            api = default_api
        self.api = api
        if _data is None:
            self.update()
        else:
            self._last_updated = time.time()

    def _make_url(self):
        """Makes the base url for each entity and uses it for api requests.
        Needs to be overwritten on each subclass
        """
        raise NotImplementedError()

    def should_update(self):
        return (
            self._last_updated is None or
            time.time() - self._last_updated > self._update_threshold
        )

    def __getitem__(self, key):
        if self.should_update():
            self.update()
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value
        self.push({key: value})

    def get(self, key, default=None):
        """Gets an attribute by key, and returns the default if not present
        """
        if self.should_update():
            self.update()
        return self._data.get(key, default)

    def push(self, data=None):
        """Push current data to the API. For updating only specific fields, use data argument.
        """
        if data is None:
            data = self._data
        self.api.call("PUT", self._make_url(), data=data)

    def update(self):
        """Synchronizes device properties with the Freedom API server.
        """
        self._data = self.api.call("GET", self._make_url())
        self._last_updated = time.time()

    def __repr__(self):
        return "<{}: {} {}>".format(
            self.__class__.__name__,
            self._id,
            self._data.get("name", "")
        )

    def __eq__(self, obj):
        return isinstance(obj, self.__class__) and obj._id == self._id
