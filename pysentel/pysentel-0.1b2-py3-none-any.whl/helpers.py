# coding: utf-8
"""
Helpers for pysentel.
"""
import configparser
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS


class PysentelConfig(object):
    """
    Module for handling configs in an easy and objected manner.
    """

    def __init__(self):
        """
        Initialization constructor - create config-object and import configs.
        """
        # Initialize configparser and the config-file
        self.config = configparser.ConfigParser()
        self.config.read('/etc/pysentel/pysentel.ini')

        try:
            self.interval = int(self.config['Pysentel']['interval'])
            self.sensors = self._get_sensors()
            self.influxdb = dict(self.config.items('InfluxDBIngest'))
        except configparser.NoSectionError:
            pass

    def _get_sensors(self) -> dict:
        """
        Internal function for extracting configured sensors
        :return: Dict of sensors with sensor_id as key and name as value.
        """
        sensors = {}
        for k, v in self.config.items('Sensors'):
            sensors[k] = v
        return sensors


class InfluxDataIngest:
    """
    Module for handling ingests to InfluxDB-bucket.
    """

    def __init__(self,
                 url: str,
                 org: str,
                 bucket: str,
                 token: str):
        """
        Initialization constructor - start our DB-connection.

        :param url: Define url for the InfluxDB connection. Required.
        :param org: Define InfluxDB organization. Required.
        :param bucket: Define InfluxDB bucket to ingest into. Required.
        :param token: Define authentication-token with write-access. Required.
        """
        self.org = org
        self.bucket = bucket
        self.url = url
        self.token = token
        self.connection = self._establish_connection()
        self.client = self._write_definitions()

    def __del__(self):
        """ Destructor for closing object correctly. """
        self._close_connection()

    def _establish_connection(self):
        """ Create connection to InfluxDB. """
        return InfluxDBClient(
            url=self.url,
            token=self.token,
            org=self.org)

    def _write_definitions(self):
        """ Define write options for write_api. """
        return self.connection.write_api(write_options=SYNCHRONOUS)

    def _close_connection(self):
        """ Closing connection to InfluxDB. """
        return self.client.close()

    def write_points(self, datapoints: list):
        """
        Write the provided datapoints to InfluxDB-bucket.

        :param datapoints: List of dictionaries for all points to be written.
            Required.
        """
        if not datapoints or not isinstance(datapoints, list):
            ValueError('Provided "datapoints" is either not provided or is '
                       'not a list.')

        return self.client.write(
            bucket=self.bucket,
            org=self.org,
            record=datapoints)
