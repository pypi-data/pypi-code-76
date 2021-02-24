# encoding: utf8
import logging
import requests
import arrow
from datetime import date
from resif_delivery_stats_plotter.errors import ApiError, NoDataError
from . import ServiceClientAbstract

logger = logging.getLogger(__name__)


class ServiceClientStatistics(ServiceClientAbstract):
    """
    Client of webservice 'statistics'
    """

    @classmethod
    def _url(cls, query_type, year=None, network=None, station=None, location=None, channel=None, media=None, type=None, country=None, month=None, sum=None, quality=None):
        """
        Builds an URL from the parameters

        :param query_type: The type of query
        :param year: The year to filter
        :param network: The network code to filter
        :param station: The station code to filter
        :param location: The location code to filter
        :param channel: The channel code to filter
        :param media: The media to filter
        :param type: The type to filter
        :param country: The country code to filter
        :param month: The month to filter
        :param sum: Sum the results
        :param quality: The quality code to filter
        :return: An URL ready to query
        :rtype: str
        """
        logger.debug('ServiceClientStatistics._url(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)' % (query_type, year, network, station, location, channel, media, type, country, month, sum, quality))

        # Parameters
        params = [
            'request=%s' % query_type,
            'format=json'
        ]
        if network:
            params.append('net=%s' % network)
        if station:
            params.append('sta=%s' % station)
        if location:
            params.append('loc=%s' % location)
        if channel:
            params.append('cha=%s' % channel)
        if media:
            params.append('media=%s' % media)
        if type:
            params.append('type=%s' % type)
        if country:
            params.append('country=%s' % country)
        if quality:
            params.append('quality=%s' % quality)
        if sum:
            params.append('sum=true')

        if year and month:
            date_start = date(year, month or 1, 1)
            date_end = arrow.get(date_start).shift(months=1).shift(days=-1).format('YYYY-MM-DD')
            params.append('start=%s' % date_start)
            params.append('end=%s' % date_end)
        elif year:
            params.append('start=%s' % date(year, 1, 1))
            params.append('end=%s' % date(year, 12, 31))

        # Build URL
        return 'http://ws.resif.fr/resifws/statistics/1/query?%s' % '&'.join(params)

    @classmethod
    def _query(cls, query_type, year=None, network=None, station=None, location=None, channel=None, media=None, type=None, country=None, month=None, sum=None, quality=None):
        """
        Run a query

        :param query_type: The type of query
        :param year: The year to filter
        :param network: The network code to filter
        :param station: The station code to filter
        :param location: The location code to filter
        :param channel: The channel code to filter
        :param media: The media to filter
        :param type: The type to filter
        :param country: The country code to filter
        :param month: The month to filter
        :param sum: Sum the results
        :param quality: The quality code to filter
        :return: The query response
        :rtype: requests.Response
        """
        logger.debug('ServiceClientStatistics._query(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)' % (query_type, year, network, station, location, channel, media, type, country, month, sum, quality))

        # Build URL
        url = cls._url(query_type, network=network, station=station, location=location, channel=channel, year=year, month=month, country=country, media=media, sum=sum, type=type, quality=quality)
        logger.debug('Querying %s', url)

        # Run query
        response = requests.get(url)
        if response.from_cache:
            logger.debug('> Using response from cached request')
        if response.status_code == 200:
            return response.json().get('datasources', {})
        if response.status_code == 204:
            logger.debug('Response %s', response)
            raise NoDataError('GET %s %i' % (url, response.status_code))
        else:
            logger.debug('Response %s', response)
            raise ApiError('GET %s %i' % (url, response.status_code))

    ####################################################################################################################
    # STANDARD QUERIES
    ##################

    @classmethod
    def send(cls, year, network=None, station=None, location=None, channel=None, media=None, month=None, country=None):
        logger.debug('ServiceClientStatistics.send(%s, %s, %s, %s, %s, %s, %s, %s)' % (year, network, station, location, channel, media, month, country))

        # Build URL
        url = cls._url('send', year, network, station, location, channel, media=media, month=month, country=country)
        logger.debug('Querying %s', url)

        # Run query
        response = requests.get(url)
        if response.from_cache:
            logger.debug('> Using response from cached request')
        if response.status_code == 200:
            if network:
                stations = {
                    'all': 0
                }
                for datasource in response.json().get('datasources'):
                    station_send = int(datasource['bytes'])
                    stations[datasource['station']] = station_send
                    stations['all'] += station_send
                return stations
            else:
                return {'all': int(response.json().get('datasources')[0]['bytes'])}
        else:
            logger.debug('Response %s', response)
            # raise ApiError('GET %s %i' % (url, response.status_code))

    @classmethod
    def timeseries(cls, year, network, station=None, location=None, channel=None, media=None, month=None):
        logger.debug('ServiceClientStatistics.timeseries(%s, %s, %s, %s, %s, %s, %s)' % (year, network, station, location, channel, media, month))
        timeseries = {}

        # Build URL
        url = cls._url('timeseries', year, network, station, location, channel, media=media, month=month)
        logger.debug('Querying %s', url)

        # Run query
        response = requests.get(url)
        if response.from_cache:
            logger.debug('> Using response from cached request')
        if response.status_code == 200:
            for datasource in response.json().get('datasources'):
                if datasource['time'] not in timeseries:
                    timeseries[datasource['time']] = {}

                timeseries[datasource['time']][datasource['country']] = {
                    'clients': datasource['clients'],
                    'bytes': datasource['bytes'],
                }

        else:
            logger.debug('Response %s', response)
            # raise ApiError('GET %s %i' % (url, response.status_code))

        return timeseries

    @classmethod
    def country(cls, year, network, station=None, location=None, channel=None, country=None, includes_all=False, month=None):
        logger.debug('ServiceClientStatistics.country(%s, %s, %s, %s, %s, %s, %s, %s)' % (year, network, station, location, channel, country, includes_all, month))
        countries = {}

        # Build URL
        url = cls._url('country', year, network, station, location, channel, country=country, month=month)
        logger.debug('Querying %s', url)

        # Run query
        response = requests.get(url)
        if response.from_cache:
            logger.debug('> Using response from cached request')
        if response.status_code == 200:
            for datasource in response.json().get('datasources'):
                if includes_all or datasource['country'] != 'all':
                    countries[datasource['country']] = {
                        'clients': datasource['clients'],
                        'requests': datasource['requests'],
                    }

        else:
            logger.debug('Response %s', response)
            # raise ApiError('GET %s %i' % (url, response.status_code))

        return countries

    @classmethod
    def storage(cls, year, network, station=None, location=None, channel=None, type='all', month=None):
        logger.debug('ServiceClientStatistics.storage(%s, %s, %s, %s, %s, %s, %s)' % (year, network, station, location, channel, type, month))

        try:
            response = cls._query('storage', network=network, station=station, location=location, channel=channel, year=year, month=month, type=type)
            # TODO
            pass

        except NoDataError:
            # TODO
            pass
        except ApiError:
            # TODO
            pass

    ####################################################################################################################
    # CUSTOM QUERIES
    ################

    @classmethod
    def requests(cls, network=None, station=None, location=None, channel=None, year=None, month=None, country='all', media=None):
        """
        Gets the requests number

        :param network: The network code to filter
        :param station: The station code to filter
        :param location: The location code to filter
        :param channel: The channel code to filter
        :param year: The year to filter
        :param month: The month to filter
        :param country: The country code to filter
        :param media: The media to filter
        :return: The number of requests
        :rtype: int
        """
        logger.debug('ServiceClientStatistics.requests(%s, %s, %s, %s, %s, %s, %s, %s)' % (network, station, location, channel, year, month, country, media))

        try:
            datasources = cls._query('country', network=network, station=station, location=location, channel=channel, year=year, month=month, media=media)

            total_requests = 0
            for datasource in datasources:
                datasource_requests = datasource.get('requests')
                if datasource_requests not in ('None', None):
                    total_requests += int(datasource_requests)

            return total_requests

        except NoDataError:
            # TODO
            pass
        except ApiError:
            # TODO
            pass

    @classmethod
    def requests_by_country(cls, network=None, station=None, location=None, channel=None, year=None, month=None, country=None, media=None):
        """
        Gets the requests number by country

        :param network: The network code to filter
        :param station: The station code to filter
        :param location: The location code to filter
        :param channel: The channel code to filter
        :param year: The year to filter
        :param month: The month to filter
        :param country: The country code to filter
        :param media: The media to filter
        :return: A dictionary of requests number grouped by country
        :rtype: dict
        """
        logger.debug('ServiceClientStatistics.requests_by_country(%s, %s, %s, %s, %s, %s, %s, %s)' % (network, station, location, channel, year, month, country, media))

        try:
            datasources = cls._query('country', network=network, station=station, location=location, channel=channel, year=year, month=month, media=media)

            countries = {}
            for datasource in datasources:
                country_code = datasource.get('country', None)
                country_requests = datasource.get('requests', None)
                if country_code not in ('None', None, 'all') and country_requests not in ('None', None):
                    countries[country_code] = int(country_requests)

            return countries

        except NoDataError:
            # TODO
            pass
        except ApiError:
            # TODO
            pass

    @classmethod
    def clients(cls, network=None, station=None, location=None, channel=None, year=None, month=None, country='all', media=None):
        """
        Gets the clients number

        :param network: The network code to filter
        :param station: The station code to filter
        :param location: The location code to filter
        :param channel: The channel code to filter
        :param year: The year to filter
        :param month: The month to filter
        :param country: The country code to filter
        :param media: The media to filter
        :return: The number of clients
        :rtype: int
        """
        logger.debug('ServiceClientStatistics.clients(%s, %s, %s, %s, %s, %s, %s, %s)' % (network, station, location, channel, year, month, country, media))

        try:
            datasources = cls._query('country', network=network, station=station, location=location, channel=channel, year=year, month=month, media=media)

            total_clients = 0
            for datasource in datasources:
                datasource_clients = datasource.get('clients')
                if datasource_clients not in ('None', None):
                    total_clients += int(datasource_clients)

            return total_clients

        except NoDataError:
            # TODO
            pass
        except ApiError:
            # TODO
            pass

    @classmethod
    def clients_by_country(cls, network=None, station=None, location=None, channel=None, year=None, month=None, country=None, media=None):
        """
        Gets the clients number by country

        :param network: The network code to filter
        :param station: The station code to filter
        :param location: The location code to filter
        :param channel: The channel code to filter
        :param year: The year to filter
        :param month: The month to filter
        :param country: The country code to filter
        :param media: The media to filter
        :return: A dictionary of clients number grouped country
        :rtype: dict
        """
        logger.debug('ServiceClientStatistics.clients_by_country(%s, %s, %s, %s, %s, %s, %s, %s)' % (network, station, location, channel, year, month, country, media))

        try:
            datasources = cls._query('country', network=network, station=station, location=location, channel=channel, year=year, month=month, media=media)

            countries = {}
            for datasource in datasources:
                country_code = datasource.get('country')
                country_clients = datasource.get('clients')
                if country_code not in ('None', None, 'all') and country_clients not in ('None', None):
                    countries[country_code] = int(country_clients)

            return countries

        except NoDataError:
            # TODO
            pass
        except ApiError:
            # TODO
            pass

    @classmethod
    def clients_and_requests_by_country(cls, network=None, station=None, location=None, channel=None, year=None, month=None, country=None, media=None):
        """
        Gets the requests and clients number by country

        :param network: The network code to filter
        :param station: The station code to filter
        :param location: The location code to filter
        :param channel: The channel code to filter
        :param year: The year to filter
        :param month: The month to filter
        :param country: The country code to filter
        :param media: The media to filter
        :return: A dictionary of requests number et clients cumber grouped by country
        :rtype: dict
        """
        logger.debug('ServiceClientStatistics.clients_and_requests_by_country(%s, %s, %s, %s, %s, %s, %s, %s)' % (network, station, location, channel, year, month, country, media))

        try:
            datasources = cls._query('country', network=network, station=station, location=location, channel=channel, year=year, month=month, media=media)

            countries = {}
            for datasource in datasources:
                country_code = datasource.get('country')
                country_clients = datasource.get('clients')
                country_requests = datasource.get('requests')
                if country_code not in ('None', None, 'all') and (country_clients not in ('None', None) or country_requests not in ('None', None)):
                    countries[country_code] = {}
                    if country_clients not in ('None', None):
                        countries[country_code]['clients'] = int(country_clients)
                    if country_requests not in ('None', None):
                        countries[country_code]['requests'] = int(country_requests)

            return countries

        except NoDataError:
            # TODO
            pass
        except ApiError:
            # TODO
            pass

    @classmethod
    def data_send(cls, network=None, station=None, location=None, channel=None, year=None, month=None, country='all', media=None, unit=None):
        """
        Gets the amount of data send

        :param network: The network code to filter
        :param station: The station code to filter
        :param location: The location code to filter
        :param channel: The channel code to filter
        :param year: The year to filter
        :param month: The month to filter
        :param country: The country code to filter
        :param media: The media to filter
        :param unit: The unit in which the result is converted ('Bytes' by default)
        :return: The amount of data send
        :rtype: int
        """
        logger.debug('ServiceClientStatistics.data_send(%s, %s, %s, %s, %s, %s, %s, %s, %s)' % (network, station, location, channel, year, month, country, media, unit))

        try:
            datasources = cls._query('send', network=network, station=station, location=location, channel=channel, year=year, month=month, media=media, sum=True)

            total_bytes = 0
            for datasource in datasources:
                datasource_bytes = datasource.get('bytes')
                if datasource_bytes not in ('None', None):
                    if unit:
                        total_bytes += cls.unit_convert(int(datasource_bytes), 'bytes', unit)
                    else:
                        total_bytes += int(datasource_bytes)

            return total_bytes

        except NoDataError:
            # TODO
            pass
        except ApiError:
            # TODO
            pass

    @classmethod
    def data_send_by_station(cls, network=None, station=None, location=None, channel=None, year=None, month=None, country='all', media=None, unit=None):
        """
        Gets the amount of data send for each station

        :param network: The network code to filter
        :param station: The station code to filter
        :param location: The location code to filter
        :param channel: The channel code to filter
        :param year: The year to filter
        :param month: The month to filter
        :param country: The country code to filter
        :param media: The media to filter
        :param unit: The unit in which the result is converted ('Bytes' by default)
        :return: A dictionary of amount of data send grouped by station code
        :rtype: dict
        """
        logger.debug('ServiceClientStatistics.data_send(%s, %s, %s, %s, %s, %s, %s, %s, %s)' % (network, station, location, channel, year, month, country, media, unit))

        try:
            datasources = cls._query('send', network=network, station=station, location=location, channel=channel, year=year, month=month, media=media)

            stations = {}
            for datasource in datasources:
                station_code = datasource.get('station')
                station_bytes = datasource.get('bytes')
                if station_code not in ('None', None, 'all') and station_bytes not in ('None', None):
                    if unit:
                        stations[station_code] = cls.unit_convert(int(station_bytes), 'bytes', unit)
                    else:
                        stations[station_code] = int(station_bytes)

            return stations

        except NoDataError:
            # TODO
            pass
        except ApiError:
            # TODO
            pass

    @classmethod
    def data_stored(cls, network=None, station=None, location=None, channel=None, year=None, month=None, quality=None, type=None, unit=None):
        """
        Gets the amount of data stored

        :param network: The network code to filter
        :param station: The station code to filter
        :param location: The location code to filter
        :param channel: The channel code to filter
        :param year: The year to filter
        :param month: The month to filter
        :param quality: The quality code to filter
        :param type: The type to filter
        :param unit: The unit in which the result is converted ('Bytes' by default)
        :return: The amount of data stored
        :rtype: int
        """
        logger.debug('ServiceClientStatistics.data_stored(%s, %s, %s, %s, %s, %s, %s, %s, %s)' % (network, station, location, channel, year, month, quality, type, unit))

        try:
            datasources = cls._query('storage', network=network, station=station, location=location, channel=channel, year=year, month=month, quality=quality, type=type)

            total_bytes = 0
            for datasource in datasources:
                datasource_size = datasource.get('size')
                if datasource_size not in ('None', None):
                    if unit:
                        total_bytes += cls.unit_convert(int(datasource_size), 'bytes', unit)
                    else:
                        total_bytes += int(datasource_size)

            return total_bytes

        except NoDataError:
            # TODO
            pass
        except ApiError:
            # TODO
            pass

    @classmethod
    def data_stored_by_quality(cls, network=None, station=None, location=None, channel=None, year=None, month=None, quality=None, type=None, unit=None):
        """
        Gets the amount of data stored for each quality

        :param network: The network code to filter
        :param station: The station code to filter
        :param location: The location code to filter
        :param channel: The channel code to filter
        :param year: The year to filter
        :param month: The month to filter
        :param quality: The quality code to filter
        :param type: The type to filter
        :param unit: The unit in which the result is converted ('Bytes' by default)
        :return: A dictionary of amount of data stored grouped by quality code
        :rtype: dict
        """
        logger.debug('ServiceClientStatistics.data_stored_by_quality(%s, %s, %s, %s, %s, %s, %s, %s, %s)' % (network, station, location, channel, year, month, quality, type, unit))

        try:
            datasources = cls._query('storage', network=network, station=station, location=location, channel=channel, year=year, month=month, quality=quality, type=type)

            qualities = {}
            for datasource in datasources:
                datasource_quality = datasource.get('quality')
                datasource_size = datasource.get('size')
                if datasource_quality not in ('None', None) and datasource_size not in ('None', None):
                    if unit:
                        qualities[datasource_quality] += cls.unit_convert(int(datasource_size), 'bytes', unit)
                    else:
                        qualities[datasource_quality] += int(datasource_size)

            return qualities

        except NoDataError:
            # TODO
            pass
        except ApiError:
            # TODO
            pass
