# encoding: utf8
import logging
from datetime import date
from resif_delivery_stats_plotter.services.clients.statistics import ServiceClientStatistics as service_stats
from .mixins import LocationCodeMixin

logger = logging.getLogger(__name__)


class Station(LocationCodeMixin):
    """
    Defines a station
    """

    def __init__(self, code=None, start_date=None, end_date=None, latitude=None, longitude=None, elevation=None, network_code=None):
        self._network_code = network_code
        self.code = code
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self._locations = {}
        self._channels = {}

        if isinstance(start_date, tuple):
            self._start_date = start_date[0]
        else:
            self._start_date = start_date

        if isinstance(end_date, tuple):
            self._end_date = end_date[0]
        else:
            self._end_date = end_date

    def __repr__(self):
        return "<Station %s (%s | %s) (%s|%s|%s) (%i locations)>" % (
            self.code,
            self.date_start, self.date_end,
            self.latitude, self.longitude, self.elevation,
            len(self._locations)
        )

    def __lt__(self, other):
        if not isinstance(other, Station):
            raise Exception("Unable to compare a 'Station' object with '%s'" % type(other))
        return self.code < other.code

    @property
    def date_start(self):
        """
        Gets the open date in ISO format for the current station

        :rtype str
        """
        if self._start_date:
            return self._start_date.isoformat()

    @property
    def date_end(self):
        """
        Gets the close date in ISO format for the current station

        :rtype str
        """
        if self._end_date:
            return self._end_date.isoformat()

    def is_open(self, year):
        """
        Checks if the station has been opened during a year

        :param year: The year to check
        :rtype: bool
        """
        if self._start_date is not None and self._start_date > date(year, 12, 31):
            return False

        if self._end_date is not None and self._end_date < date(year, 1, 1):
            return False

        return True

    @property
    def is_still_active(self):
        """
        Check s if the station is still active
        :rtype: bool
        """
        return self.is_open(2500)

    # LOCATIONS
    ####################################################################################################################

    def get_location(self, code):
        """
        Gets, and initializes if needed, a sub-collection by location code from the current collection

        :param code: The location code
        :return: A collection of channels
        :type: StationLocation
        """
        if code not in self._locations:
            location = StationLocation(code)
            self._locations[location.code] = location
        else:
            location = self._locations.get(code)
        return location

    # CHANNELS
    ####################################################################################################################

    def filter_channels(self, location=None, band=None, instrument=None, orientation=None):
        """
        Filters channels of the current collection

        :param location: The code of the location to filter the channels
        :param band: The code of the band to filter the channels
        :param instrument: The code of the instrument to filter the channels
        :param orientation: The code of the instrument's orientation to filter the channels
        :return: A selection of channels for the current station
        :rtype: list
        """
        channels = []

        for channel in self.channels:
            if location:
                if isinstance(location, (list, tuple)):
                    if channel.location not in location:
                        continue
                else:
                    if channel.location != location:
                        continue

            if band:
                if isinstance(band, (list, tuple)):
                    if channel.band not in band:
                        continue
                else:
                    if channel.band != band:
                        continue

            if instrument:
                if isinstance(instrument, (list, tuple)):
                    if channel.instrument not in instrument:
                        continue
                else:
                    if channel.instrument != instrument:
                        continue

            if orientation:
                if isinstance(orientation, (list, tuple)):
                    if channel.orientation not in orientation:
                        continue
                else:
                    if channel.orientation != orientation:
                        continue

            channels.append(channel)

        return channels

    def active_channels(self, year):
        """
        Gets the active channels of the current station during a defined year

        :param year: The year during which the channels have to be opened
        :return: A selection of channels
        :rtype: dict
        """
        active_channels = {}

        def check_channels(channels):
            for channel in channels.values():
                if channel.is_open(year):
                    active_channels[channel.location_code] = channel

        if self._locations:
            for location in self._locations.values():
                check_channels(location.channels)
        else:
            check_channels(self._channels)

        return active_channels

    def grouped_active_channels(self, year, group_location=True, group_band=True, group_instrument=True, group_orientation=False):
        """
        Gets the active channels of the current station during a defined year, and grouped by '<location>.<band><instrument>'

        :param year: The year during which the channels have to be opened
        :param group_location: Use location code to group channels
        :param group_band: Use band code to group channels
        :param group_instrument: Use instrument code to group channels
        :param group_orientation: Use orientation code to group channels
        :return: A selection of channels
        :rtype: dict
        """
        groups = {}

        def check_channels(channels):
            for channel in channels.values():
                if channel.is_open(year):
                    group_code = channel.custom_code(group_location, group_band, group_instrument, group_orientation)
                    if group_code not in groups:
                        groups[group_code] = {}

                    groups[group_code][channel.location_code] = channel

        if self._locations:
            for location in self._locations.values():
                check_channels(location.channels)
        else:
            check_channels(self._channels)

        return groups

    def add_channel(self, channel):
        """
        Adds a channel to the current station

        :param channel: The channel to add
        """
        channel._network_code = self._network_code
        channel._station_code = self.code
        if channel.has_location:
            location = self.get_location(channel.location)
            location.add_channel(channel)
        else:
            self._channels[channel.code] = channel

    def get_channel(self, location_code):
        """
        Gets a channel by its location code from the current station

        :param location_code: The location code of the channel to get
        :return: A channel
        :rtype: Channel
        """
        loc = self.extract_location_from_location_code(location_code)
        if loc:
            location = self._locations.get(loc)
            if location:
                return location.get_channel(location_code)

        return self._channels.get(location_code)

    @property
    def channels(self):
        """
        Gets the channels of the current station

        :return: A list of channel
        :rtype: list
        """
        if self._locations:
            channels = []
            for location_channels in self._locations.values():
                channels.extend(location_channels.values())
            return sorted(channels)
        else:
            return sorted(self._channels.values())

    def representative_channels(self, year=None, month=None, quality=None):
        """
        Gets the representative channel of the current station

        :param year: The year to filter
        :param month: The month to filter
        :param quality: The quality to filter
        :return: A selection of representative channels
        :rtype: list
        """
        if self._locations:
            representative_channels = []
            for location in self._locations.values():
                location_channel = location.representative_channel(year, month, quality)
                if location_channel:
                    representative_channels.append(location_channel)

            if not representative_channels:
                logger.warning("No representative channel found for station %s" % self.code)
            return representative_channels

        elif self._channels:
            for channel in sorted(self._channels.values()):
                if channel.check_availability(year, month, quality):
                    return [channel, ]
            logger.warning("No representative channel found for station %s" % self.code)
        else:
            logger.warning("No representative channel found for station %s" % self.code)
            return []

    # STATISTICS
    ####################################################################################################################

    def requests(self, year=None, month=None, country=None, media=None):
        """
        Get the requests number for the current station

        :param year: The year to filter the requests
        :param month:  The month to filter the requests
        :param country:  The country to filter the requests
        :param media:  The media to filter the requests
        :return: The requests number
        :rtype: int
        """
        return service_stats.requests(network=self._network_code, station=self.code, year=year, month=month, country=country, media=media)

    def requests_by_country(self, year=None, month=None, country=None, media=None):
        """
        Get the requests number for each country, for the current station

        :param year: The year to filter the requests
        :param month:  The month to filter the requests
        :param country:  The country to filter the requests
        :param media:  The media to filter the requests
        :return: The requests number
        :rtype: int
        """
        return service_stats.requests_by_country(network=self._network_code, station=self.code, year=year, month=month, country=country, media=media)

    def clients(self, year=None, month=None, country=None, media=None):
        """
        Get the clients number for the current station

        :param year: The year to filter the clients
        :param month:  The month to filter the clients
        :param country:  The country to filter the clients
        :param media:  The media to filter the clients
        :return: The clients number
        :rtype: int
        """
        return service_stats.clients(network=self._network_code, station=self.code, year=year, month=month, country=country, media=media)

    def clients_by_country(self, year=None, month=None, country=None, media=None):
        """
        Get the clients number for each country, for the current station

        :param year: The year to filter the clients
        :param month:  The month to filter the clients
        :param country:  The country to filter the clients
        :param media:  The media to filter the clients
        :return: The clients number
        :rtype: int
        """
        return service_stats.clients_by_country(network=self._network_code, station=self.code, year=year, month=month, country=country, media=media)

    def data_send(self, year=None, month=None, country=None, media=None, unit=None):
        """
        Gets the amount of data send for the current station

        :param year: The year to filter the stats
        :param month:  The month to filter the stats
        :param country:  The country to filter the stats
        :param media:  The media to filter the stats
        :param unit: The unit to convert the result into (default: 'Bytes')
        :return: The amount of data send
        :rtype: int
        """
        return service_stats.data_send(network=self._network_code, station=self.code, year=year, month=month, country=country, media=media, unit=unit)

    def data_send_dataselect(self, year=None, month=None, country=None, unit=None):
        """
        Gets the amount of data send by dataselect for the current station

        :param year: The year to filter the stats
        :param month:  The month to filter the stats
        :param country:  The country to filter the stats
        :param unit: The unit to convert the result into (default: 'Bytes')
        :return: The amount of data send by dataselect
        :rtype: int
        """
        return self.data_send(year=year, month=month, country=country, media='dataselect', unit=unit)

    def data_send_seedlink(self, year, month=None, country=None, unit=None):
        """
        Gets the amount of data send by seedlink for the current station

        :param year: The year to filter the stats
        :param month:  The month to filter the stats
        :param country:  The country to filter the stats
        :param unit: The unit to convert the result into (default: 'Bytes')
        :return: The amount of data send by seedlink
        :rtype: int
        """
        return self.data_send(year=year, month=month, country=country, media='seedlink', unit=unit)

    def data_send_station(self, year, month=None, country=None, unit=None):
        """
        Gets the amount of data send by station WS for the current station

        :param year: The year to filter the stats
        :param month:  The month to filter the stats
        :param country:  The country to filter the stats
        :param unit: The unit to convert the result into (default: 'Bytes')
        :return: The amount of data send by station WS
        :rtype: int
        """
        return self.data_send(year=year, month=month, country=country, media='station', unit=unit)


class StationLocation(LocationCodeMixin):
    """
    Defines a location to group channels of a station
    """

    def __init__(self, code):
        self.code = code
        self.channels = {}

    def __repr__(self):
        return "<StationLocation %s (%i channels)>" % (
            self.code,
            len(self.channels)
        )

    def add_channel(self, channel):
        """
        Adds a channel to the current collection

        :param channel: The channel to add
        """
        self.channels[channel.location_code] = channel

    def get_channel(self, location_code):
        """
        Gets a channel by its location code from the current collection

        :param location_code: The location code of the channel to get
        :return: A channel
        :rtype: Channel
        """
        return self.channels.get(location_code)

    def representative_channel(self, year=None, month=None, quality=None):
        """
        Gets the representative channel of the current collection

        :param year: The year to filter
        :param month: The month to filter
        :param quality: The quality to filter
        :return: The representative channel
        :rtype: Channel
        """
        if self.channels:
            for channel in sorted(self.channels.values()):
                if channel.check_availability(year, month, quality):
                    return channel

    def open_channels(self, year, as_list=False):
        """
        Gets the opened channels during a year

        :param year: The year during which the channels have to be opened
        :param as_list: Change the return type to list instead of dict
        :return: The channels opened during a year
        :rtype: dict|list
        """
        channels = {}
        for channel in sorted(self.channels.values()):
            if channel.is_open(year):
                channels[channel.location_code] = channel

        if as_list:
            return sorted(channels.values())

        return channels
