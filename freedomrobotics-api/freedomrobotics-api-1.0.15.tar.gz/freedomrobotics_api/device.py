import json
import time
import logging

from .alert import Alert
from .entity import Entity
from .helpers import to_unix_time

logger = logging.getLogger(__name__)


class Device(Entity):

    def _make_url(self):
        return "/accounts/{}/devices/{}".format(self.account, self._id)

    def command(self, topic=None, topic_type=None, data=None, expiration_secs=10, platform="ros"):
        cmd = {
            "topic": topic,
            "type": topic_type,
            "data": data,
            "expiration_secs": expiration_secs,
            "platform": platform,
        }
        return self.api.call(
            "PUT",
            "/accounts/{}/devices/{}/commands".format(self.account, self._id),
            data=cmd
        )

    @property
    def cloned_from(self):
        """Where the device was cloned from.
        """
        return self._data.get("clonedFrom")

    @property
    def compute_architecture(self):
        """str: Compute architecture.
        """
        return self._data.get("compute_architecture")

    def create_token(self, params=None):
        """dict: Creates a token and returns the response.
        Args:
            params (dict): Optional query parameters.
        """
        response = self.api.call(
            "POST",
            "/tokens?create_secret=true",
            data={
                "allowed_actions": {
                    "install_script": ["get"],
                    "download": ["get"],
                    "device": ["get", "put"],
                    "device_data": ["put"],
                    "device_commands": ["get"],
                },
                "accounts": [self.account],
                "devices": [self._id],
            },
            params=params,
        )

        if response.get("status") == "success":
            return response
        else:
            return None

    @property
    def account(self):
        return self._data.get('account')

    @property
    def description(self):
        """str: Description of the device.
        """
        return self._data.get("description")

    @property
    def name(self):
        """str: Name of the device.
        """
        return self._data.get("name")

    @property
    def features(self):
        """:obj:`list` of `str`: features of the device.
        """
        return self._data.get("features")

    def get_attr(self, key):
        """Fetches a custom attribute."""

        return self.get(key)

    def set_attr(self, key, value):
        """Sets a custom attribute."""
        self[key] = value

    def set_attrs(self, attrs):
        """Sets multiple custom attributes."""
        self.push(attrs)

    @property
    def platform(self):
        """str: Platform of the device.
        """
        return self._data.get("platform")

    @property
    def device_type(self):
        """str: Device type.
        """
        return self._data.get("type")

    @property
    def mc_alerts_enabled(self):
        """`list`: Alerts enabled for the device.
        """
        return self._data.get("mc.alerts.enabled")

    @property
    def mc_alerts_triggers(self):
        """`list`: Alert triggers.
        """
        return self._data.get("mc.alerts.triggers")

    @property
    def mc_alerts_triggered(self):
        """`list` of :obj:`Alert`: List of alerts that are triggered.
        """
        result = self._data.get("mc.alerts.triggered")
        if not result:
            return []

        alerts = [Alert(alert__data["alert_id"], alert__data) for alert__data in result]
        return alerts

    @property
    def mc_instrumentation_remote_ssh(self):
        """`dict`: Information about currently active SSH reverse port forward.
        Use enable_remote_ssh() to enable ssh.
        """
        return self._data.get("mc.instrumentation.remote_ssh")

    def enable_remote_ssh(self):
        """Enables remote SSH on the device. Following this method,
        periodically .update() the device and check for updates in
        .mc_instrumentation_remote_ssh() for the connection information.
        """
        data = [
            {
                "command": "enable_remote_ssh",
                "platform": "mission_control_controller",
                "expiration_secs": 100,
                "data": {"enable": True},
                "uid": "AEFF321AEF56ECD"
            },
        ]

        response = self.api.call(
            "PUT",
            "/accounts/%s/devices/%s/commands" % (
                self._data.get("account"),
                self._id
            ),
            data=data
        )

        return response

    def data(self, start=None, end=None, topics=None, direction="forward", **params):
        """iter: Fetches data from the robot for a specified interval and returns an iterator
        to page through the data. Each next() call to the iterator will return 1 message, and
        data will be fetched from the server as necessary until the end has been reached.

        Args:
            start (float): UNIX time of the start of the desired data interval.
            end (float): UNIX time of the end of the desired data interval.
            topics (`list` of `str`): List of topics of interest (in most cases, ROS topics).
            direction (str): "forward" or "backward".
        """
        if start is not None:
            params["utc_start"] = to_unix_time(start)
            if end is None:
                params["utc_end"] = to_unix_time(start) + 60.0
            else:
                params["utc_end"] = to_unix_time(end)

        if topics is not None:
            params["topics"] = json.dumps(topics)

        params["pagination"] = True
        params["pagination_direction"] = direction

        while True:
            result = self.api.call(
                "GET",
                "/accounts/{}/devices/{}/data/".format(self.account, self._id),
                params=params
            )

            # sort messages in case server returns messages in wrong order
            # (not sure if necessary but API doc doesn't seem to guarantee it)
            if direction == "forward":
                result["messages"].sort(key=lambda item: item.get("utc_time", 0.0))
            else:
                result["messages"].sort(key=lambda item: item.get("utc_time", 0.0), reverse=True)

            if result is None or len(result["messages"]) == 0:
                return

            logger.debug("fetched %d of %d messages" % (
                result.get("returned_num_messages", -1), result.get("requested_num_messages", -1)
            ))

            if not result.get("returned_utc_start") or not result.get("returned_utc_end"):
                return

            for item in result.get("messages", {}):
                logger.debug("item: ", item)
                yield item

            if direction == "forward":
                params["utc_start"] = result.get("returned_utc_end")
                params["utc_end"] = min(
                    params["utc_start"] + 1.1 * (result.get("returned_utc_end") - result.get("returned_utc_start")),
                    end
                )
            elif direction == "backward":
                params["utc_end"] = result.get("returned_utc_start")
                params["utc_start"] = max(
                    params["utc_end"] - 1.1 * (result.get("returned_utc_end") - result.get("returned_utc_start")),
                    start
                )

    def data_last(self, topics=None):
        """Returns the last message published by the device, as long as it is within the past 1 minute.

        Args:
            topics (`list` of `str`): Topics of interest.
        """
        params = {}
        params["one_message_per_topic"] = "true"
        params["utc_start"] = to_unix_time(time.time() - 60.0)
        params["utc_end"] = to_unix_time(time.time())

        if topics is not None:
            params["topics"] = json.dumps(topics)

        result = self.api.call(
            "GET",
            "/accounts/{}/devices/{}/statistics/".format(self.account, self._id),
            params=params
        )

        if result is None or len(result) == 0:
            return None

        # sort messages in case server returns messages in wrong order
        # (not sure if necessary but API doc doesn't seem to guarantee it)
        result.sort(key=lambda item: item.get("utc_time", 0.0))

        return result[-1]

    def get_statistics(self, utc_start=None, utc_end=None, params=None):
        """GET statistics endpoint abstraction.

        Args:
            utc_start (float): Returns statistics starting from the specified timestamp.
                       If null, returns the API default range (1 day).
            utc_end (float): Returns statistics until the specified timestamp (inclusive).
                       If null, returns the statistics until current hour.
            params (dict): Extra parameters that could be included in the request.

        Returns:
            Dictionary with utc timestamp hourly rounded as keys, and the calculated statistics
            for each hour.
            Note: The current hour will always return a partial result that might have a couple of
                  minutes of delay depending on the statistic type.
        """

        if params is None:
            params = {}
        if utc_start is not None:
            params["utc_start"] = utc_start
        if utc_end is not None:
            params["utc_end"] = utc_end

        result = self.api.call(
            "GET",
            "/accounts/{}/devices/{}/statistics/".format(self.account, self._id),
            params=params
        )
        return result

    def put_statistics(self, data, params=None):
        """PUT statistics endpoint abstraction

        Args:
            data (list): List with dictionaries with statistics values per hour.
            More info about the object format can be found on API docs:
            https://docs.freedomrobotics.ai/reference#rest-api
            params (dict): Extra parameters that could be included in the request.
        """
        self.api.call(
            "PUT",
            "/accounts/{}/devices/{}/statistics/".format(self.account, self._id),
            data=data,
            params=params,
        )
