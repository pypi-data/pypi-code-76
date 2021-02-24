
from .entity import Entity


class Zone(Entity):

    def _make_url(self):
        return "/accounts/{}/zones/{}".format(self._data.get('account_id'), self._id)

    @property
    def name(self):
        """str: Account name.
        """
        return self._data.get("name")

    @property
    def sub_zones(self):
        """:obj:`list` of :obj:`Zone`: Fetch a list of all zones in the account.
        """
        if not self._data.get("has_subzones"):
            return []
        return [Zone(data['id'], data, api=self.api) for data in self._data.get("sub_zones", [])]
