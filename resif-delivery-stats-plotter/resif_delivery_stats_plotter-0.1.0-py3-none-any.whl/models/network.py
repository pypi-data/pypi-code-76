# encoding: utf8
from resif_delivery_stats_plotter.services.clients.statistics import ServiceClientStatistics as service_stats


class Network:
    """
    Defines a network
    """

    def __init__(self, code=None, start_date=None, end_date=None, stations=None):
        self.code = code
        self._stations = stations or {}

        if isinstance(start_date, tuple):
            self._start_date = start_date[0]
        else:
            self._start_date = start_date

        if isinstance(end_date, tuple):
            self._end_date = end_date[0]
        else:
            self._end_date = end_date

    def __repr__(self):
        return "<Network %s (%s | %s)>" % (
            self.code,
            self.date_start, self.date_end,
        )

    @property
    def date_start(self):
        """
        Gets the open date in ISO format for the current network

        :rtype str
        """
        if self._start_date:
            return self._start_date.isoformat()

    @property
    def date_end(self):
        """
        Gets the close date in ISO format for the current network

        :rtype str
        """
        if self._end_date:
            return self._end_date.isoformat()

    @property
    def year_start(self):
        """
        Gets the open year for the current network

        :rtype str
        """
        if self._start_date:
            return self._start_date.year

    # STATIONS
    ####################################################################################################################

    def add_station(self, station):
        """
        Adds a station to the current network

        :param station: The station to add
        """
        if station is not None:
            station._network_code = self.code
            self._stations[station.code] = station

    def get_station(self, code):
        """
        Gets a station by its code from the current network

        :param code: The code of the station to get
        :return: A station
        :rtype: Station
        """
        return self._stations.get(code)

    @property
    def stations(self):
        """
        Gets the list of stations of the current network

        :return: A collection of stations
        :rtype: list
        """
        return sorted(self._stations.values())

    def active_stations(self, year):
        """
        Gets the list of active stations of the current network

        :return: A collection of stations
        :rtype: list
        """
        stations = []
        for station in self.stations:
            if station.is_open(year):
                stations.append(station)
        return stations

    # STATISTICS
    ####################################################################################################################

    def requests(self, year=None, month=None, country=None, media=None):
        """
        Get the requests number for the current network

        :param year: The year to filter the requests
        :param month:  The month to filter the requests
        :param country:  The country to filter the requests
        :param media:  The media to filter the requests
        :return: The requests number
        :rtype: int
        """
        return service_stats.requests(network=self.code, year=year, month=month, country=country, media=media)

    def requests_seedlink(self, year=None, month=None, country=None):
        """
        Get the requests number querying seedlink for the current network

        :param year: The year to filter the requests
        :param month:  The month to filter the requests
        :param country:  The country to filter the requests
        :return: The requests number
        :rtype: int
        """
        return self.requests(year=year, month=month, country=country, media='seedlink')

    def requests_dataselect(self, year=None, month=None, country=None):
        """
        Get the requests number querying dataselect for the current network

        :param year: The year to filter the requests
        :param month:  The month to filter the requests
        :param country:  The country to filter the requests
        :return: The requests number
        :rtype: int
        """
        return self.requests(year=year, month=month, country=country, media='dataselect')

    def requests_station(self, year=None, month=None, country=None):
        """
        Get the requests number querying station for the current network

        :param year: The year to filter the requests
        :param month:  The month to filter the requests
        :param country:  The country to filter the requests
        :return: The requests number
        :rtype: int
        """
        return self.requests(year=year, month=month, country=country, media='station')

    def requests_by_country(self, year=None, month=None, country=None, media=None):
        """
        Get the requests number for each country, for the current network

        :param year: The year to filter the requests
        :param month:  The month to filter the requests
        :param country:  The country to filter the requests
        :param media:  The media to filter the requests
        :return: The requests number
        :rtype: int
        """
        return service_stats.requests_by_country(network=self.code, year=year, month=month, country=country, media=media)

    def requests_seedlink_by_country(self, year=None, month=None, country=None):
        """
        Get the requests number for each country, querying seedlink for the current network

        :param year: The year to filter the clients
        :param month:  The month to filter the clients
        :param country:  The country to filter the clients
        :return: The clients number
        :rtype: int
        """
        return self.requests_by_country(year=year, month=month, country=country, media='seedlink')

    def requests_dataselect_by_country(self, year=None, month=None, country=None):
        """
        Get the requests number for each country, querying dataselect for the current network

        :param year: The year to filter the clients
        :param month:  The month to filter the clients
        :param country:  The country to filter the clients
        :return: The clients number
        :rtype: int
        """
        return self.requests_by_country(year=year, month=month, country=country, media='dataselect')

    def requests_station_by_country(self, year=None, month=None, country=None):
        """
        Get the requests number for each country, querying station for the current network

        :param year: The year to filter the clients
        :param month:  The month to filter the clients
        :param country:  The country to filter the clients
        :return: The clients number
        :rtype: int
        """
        return self.requests_by_country(year=year, month=month, country=country, media='station')

    def clients(self, year=None, month=None, country=None, media=None):
        """
        Get the clients number for the current network

        :param year: The year to filter the clients
        :param month:  The month to filter the clients
        :param country:  The country to filter the clients
        :param media:  The media to filter the clients
        :return: The clients number
        :rtype: int
        """
        return service_stats.clients(network=self.code, year=year, month=month, country=country, media=media)

    def clients_by_country(self, year=None, month=None, country=None, media=None):
        """
        Get the clients number for each country, for the current network

        :param year: The year to filter the clients
        :param month:  The month to filter the clients
        :param country:  The country to filter the clients
        :param media:  The media to filter the clients
        :return: The clients number
        :rtype: int
        """
        return service_stats.clients_by_country(network=self.code, year=year, month=month, country=country, media=media)

    def clients_seedlink_by_country(self, year=None, month=None, country=None):
        """
        Get the clients number for each country, requesting seedlink for the current network

        :param year: The year to filter the clients
        :param month:  The month to filter the clients
        :param country:  The country to filter the clients
        :return: The clients number
        :rtype: int
        """
        return self.clients_by_country(year=year, month=month, country=country, media='seedlink')

    def clients_dataselect_by_country(self, year=None, month=None, country=None):
        """
        Get the clients number for each country, requesting dataselect for the current network

        :param year: The year to filter the clients
        :param month:  The month to filter the clients
        :param country:  The country to filter the clients
        :return: The clients number
        :rtype: int
        """
        return self.clients_by_country(year=year, month=month, country=country, media='dataselect')

    def clients_station_by_country(self, year=None, month=None, country=None):
        """
        Get the clients number for each country, requesting station for the current network

        :param year: The year to filter the clients
        :param month:  The month to filter the clients
        :param country:  The country to filter the clients
        :return: The clients number
        :rtype: int
        """
        return self.clients_by_country(year=year, month=month, country=country, media='station')

    def data_send(self, year=None, month=None, country=None, media=None, unit=None):
        """
        Gets the amount of data send for the current network

        :param year: The year to filter the stats
        :param month:  The month to filter the stats
        :param country:  The country to filter the stats
        :param media:  The media to filter the stats
        :param unit: The unit to convert the result into (default: 'Bytes')
        :return: The amount of data send
        :rtype: int
        """
        return service_stats.data_send(network=self.code, year=year, month=month, country=country, media=media, unit=unit)

    def data_send_dataselect(self, year=None, month=None, country=None, unit=None):
        """
        Gets the amount of data send by dataselect for the current network

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
        Gets the amount of data send by seedlink for the current network

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
        Gets the amount of data send by station WS for the current network

        :param year: The year to filter the stats
        :param month:  The month to filter the stats
        :param country:  The country to filter the stats
        :param unit: The unit to convert the result into (default: 'Bytes')
        :return: The amount of data send by station WS
        :rtype: int
        """
        return self.data_send(year=year, month=month, country=country, media='station', unit=unit)

    def data_stored(self, year=None, month=None, quality=None, type=None, unit=None):
        """
        Gets the amount of data stored for the current network

        :param year: The year to filter the stats
        :param month:  The month to filter the stats
        :param quality:  The quality to filter the stats
        :param type:  The type to filter the stats
        :param unit: The unit to convert the result into (default: 'Bytes')
        :return: The amount of data send
        :rtype: int
        """
        return service_stats.data_stored(network=self.code, year=year, month=month, quality=quality, type=type, unit=unit)

    def data_stored_buffer(self, year=None, month=None, quality=None, unit=None):
        """
        Gets the amount of 'buffer' data stored for the current network

        :param year: The year to filter the stats
        :param month:  The month to filter the stats
        :param quality:  The quality to filter the stats
        :param unit: The unit to convert the result into (default: 'Bytes')
        :return: The amount of data send
        :rtype: int
        """
        return self.data_stored(year=year, month=month, quality=quality, type='buffer', unit=unit)

    def data_stored_validated(self, year=None, month=None, quality=None, unit=None):
        """
        Gets the amount of 'validated' data stored for the current network

        :param year: The year to filter the stats
        :param month:  The month to filter the stats
        :param quality:  The quality to filter the stats
        :param unit: The unit to convert the result into (default: 'Bytes')
        :return: The amount of data send
        :rtype: int
        """
        return self.data_stored(year=year, month=month, quality=quality, type='validated', unit=unit)
