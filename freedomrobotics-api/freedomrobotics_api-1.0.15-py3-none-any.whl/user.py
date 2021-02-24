from .account import Account
from .entity import Entity


class User(Entity):
    """A user within the Freedom Robotics API. Not intended to be manually instantiated by the user of the API.

    Args:
        _id (str): User ID (e-mail address).
        _data (`dict`): User data.
    """

    def __repr__(self):
        return "<User: %s %s %s>" % (
            self._id,
            self._data.get("first_name", ""),
            self._data.get("last_name",  ""),
        )

    def _make_url(self):
        return "/users/{}".format(self._id)

    @property
    def first_name(self):
        return self._data.get("first_name")

    @property
    def role(self):
        return self._data.get("role")

    @property
    def accounts(self):
        return [Account(account_id, None, api=self.api) for account_id in self._data["accounts"]]
