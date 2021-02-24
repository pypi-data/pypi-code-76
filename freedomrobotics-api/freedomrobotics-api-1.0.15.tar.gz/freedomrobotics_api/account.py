import json

from .device import Device
from .entity import Entity
from .zone import Zone


class Account(Entity):
    """An account within the Freedom Robotics API. Normally fetched from a :obj:`FreedomClient`
    and not intended to be manually instantiated by the user of the API.

    Args:
        _id (str): Account ID.
        _data (`dict`): Account data.
    """

    def _make_url(self):
        return "/accounts/{}".format(self._id)

    @property
    def company(self):
        """str: The company or organization of the account.
        """
        return self._data.get("company")

    def find_device(self, name=""):
        """:obj:`Device`: Finds a device by its name (i.e. the name set in the Freedom web app).
        Case-insensitive.
        If there are no matches, or there is more than one match, an exception will be thrown.

        Args:
            name (str): The name of the device.
        """

        devices = [device for device in self.get_devices() if device.name.lower() == name.lower()]

        if len(devices) == 0:
            raise Exception("No device found")

        if len(devices) > 1:
            raise Exception("Multiple devices found")

        return devices[0]

    def create_device(self, name="default", description="", device_type="", location="", platform="ros"):
        """:obj:`Device`: Creates a new device.

        Args:
            name (str): Device name.
            description (str): Device description.
            device_type (str): Device type.
            location (str): Device location.
            platform (str): Device platform.
        """

        response = self.api.call(
            "POST",
            "/accounts/{}/devices".format(self._id),
            data={
                "name": name,
                "description": description,
                "type": device_type,
                "location": location,
                "platform": platform,
            }
        )

        if response and response.get("status") != "success":
            raise Exception("create device error: {}".format(response))

        return self.get_device(response.get("device"))

    def get_device(self, device_id, params=None):
        """:obj:`Device`: Fetch an device by its device ID (Dxxxxxxxxxxxx).

        Args:
            device_id (str): Device ID.
            params (dict): Optional query parameters.
        """

        device_data = self.api.call(
            "GET",
            "/accounts/{}/devices/{}".format(self._id, device_id),
            params=params,
        )
        if not device_data:
            return None

        device = Device(device_data["device"], device_data, api=self.api)
        return device

    def get_devices(self, attributes=None, zones=None, include_subzones=None, params=None):
        """:obj:`list` of :obj:`Device`: Fetch a list of all devices in the account.

        Args:
            device_id (str): Device ID.
            attributes (list): Optional list of device attributes to return.
            attributes (zones): Optional list of zones to filter.
            include_subzones (zones): Optional list of subzones to filter.
            params (dict): Optional query parameters.
        """

        if params is None:
            params = {}
        if attributes is not None:
            params["attributes"] = json.dumps(attributes)
        if zones is not None:
            params["zones"] = json.dumps(zones)
        if include_subzones is not None:
            params["include_subzones"] = json.dumps(include_subzones)

        result = self.api.call("GET", "/accounts/{}/devices".format(self._id), params=params)
        if not isinstance(result, list):
            raise ValueError("API returned incorrect type")
        return [Device(device_data["device"], device_data, api=self.api) for device_data in result]

    def get_zones(self, params=None):
        """:obj:`list` of :obj:`Zone`: Fetch a list of all zones in the account.

        Args:
            params (dict): Optional query parameters.
        """
        result = self.api.call(
            "GET",
            "/accounts/{}/zones".format(self._id),
            params=params,
        )
        if not result:
            return []
        return [Zone(data['id'], data, api=self.api) for data in result]

    @property
    def email(self):
        """str: Account e-mail address.
        """
        return self._data.get("email")

    @property
    def features(self):
        """str: Account features.
        """
        return self._data.get("features")

    @property
    def last_seen(self):
        """float: Unix time the account was last seen.
        """
        return self._data.get("last_seen")

    @property
    def max_devices(self):
        """int: Maximum number of devices in the account.
        """
        return self._data.get("max_devices")

    @property
    def name(self):
        """str: Account name.
        """
        return self._data.get("name")

    def get_statistics_csv(self, utc_start=None, utc_end=None, params=None):
        """Gets all the statistics for an account in a CSV format.

        Args:
            utc_start (float): Returns statistics starting from the specified timestamp.
                If null, returns the API default range (1 day).
            utc_end (float): Returns statistics until the specified timestamp (inclusive).
                If null, returns the statistics until current hour.
            params (dict): Extra parameters that could be included in the request.

        Returns:
            String object with the CSV content.
        """
        if params is None:
            params = {}
        if utc_start is not None:
            params['utc_start'] = utc_start
        if utc_end is not None:
            params['utc_end'] = utc_end

        data = self.api.call(
            "GET",
            "/accounts/{}/statistics/csv".format(self._id),
            raw=True,
            params=params,
        )
        return data
