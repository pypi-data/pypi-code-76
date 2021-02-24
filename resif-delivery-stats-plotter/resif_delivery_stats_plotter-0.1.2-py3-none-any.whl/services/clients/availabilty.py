# encoding: utf8
import logging
import requests
import arrow
from datetime import date
from resif_delivery_stats_plotter.errors import ApiError
from . import ServiceClientAbstract

logger = logging.getLogger(__name__)


class ServiceClientAvailability(ServiceClientAbstract):
    """
    Client of webservice 'availability'
    """

    QUALITY_D_INDETERMINATE = 'D'
    QUALITY_R_RAW = 'R'
    QUALITY_Q_CONTROLLED = 'Q'
    QUALITY_M_MODIFIED = 'M'

    @classmethod
    def _url(cls, network=None, station=None, location=None, channel=None, year=None, month=None, quality=None):
        """
        Builds an URL from the parameters

        :param network: The network code to filter
        :param station: The station code to filter
        :param location: The location code to filter
        :param channel: The channel code to filter
        :param year: The year to filter
        :param month: The month to filter
        :param quality: The quality code to filter
        :return: An URL ready to query
        :rtype: str
        """
        logger.debug('ServiceClientAvailability._url(%s, %s, %s, %s, %s, %s, %s)' % (network, station, location, channel, year, month, quality))

        # Parameters
        params = [
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
        if quality:
            params.append('quality=%s' % channel)

        if year and month:
            date_start = date(year, month or 1, 1)
            date_end = arrow.get(date_start).shift(months=1).shift(days=-1).format('YYYY-MM-DD')
            params.append('start=%s' % date_start)
            params.append('end=%s' % date_end)
        elif year:
            params.append('start=%s' % date(year, 1, 1))
            params.append('end=%s' % date(year, 12, 31))

        # Build URL
        return 'http://ws.resif.fr/fdsnws/availability/1/query?%s' % '&'.join(params)

    @classmethod
    def channel(cls, channel, location, station, network, year, month=None, quality=None):
        """
        Gets the availability of a channel

        :param channel: The channel code to filter
        :param location: The location code to filter
        :param station: The station code to filter
        :param network: The network code to filter
        :param year: The year to filter
        :param month: The month to filter
        :param quality: The quality to filter
        :return: A collection of availability periods grouped by quality
        :rtype: dict
        """
        logger.debug('ServiceClientAvailability.channel(%s, %s, %s, %s, %s, %s, %s)' % (channel, location, station, network, year, month, quality))

        # Build URL
        url = cls._url(network, station, location, channel, year, month=month, quality=quality)
        logger.debug('Querying %s', url)

        # Run query
        response = requests.get(url)
        if response.from_cache:
            logger.debug('> Using response from cached request')
        if response.status_code == 200:
            channel_qualities = {}
            item = response.json()
            for datasource in item.get('datasources'):
                if datasource.get('quality') not in channel_qualities:
                    channel_qualities[datasource.get('quality')] = []

                for timespan in datasource.get('timespans'):
                    channel_qualities[datasource.get('quality')].append(timespan)
                    #print("Availability: from %s to %s" % (timespan[0], timespan[1]))

            return channel_qualities

        else:
            logger.debug('Response %s', response)
            # raise ApiError('GET %s %i' % (url, response.status_code))

    @classmethod
    def check_channel(cls, channel, location, station, network, year, month=None, quality=None):
        """
        Checks the availability of a channel

        :param channel: The channel code to filter
        :param location: The location code to filter
        :param station: The station code to filter
        :param network: The network code to filter
        :param year: The year to filter
        :param month: The month to filter
        :param quality: The quality to filter
        :return: Boolean flag telling if 'availability' stats are available
        :rtype: bool
        """
        logger.debug('ServiceClientAvailability.check_channel(%s, %s, %s, %s, %s, %s, %s)' % (channel, location, station, network, year, month, quality))

        # Build URL
        url = cls._url(network, station, location, channel, year, month=month, quality=quality)
        logger.debug('Querying %s', url)

        # Run query
        response = requests.get(url)
        if response.from_cache:
            logger.debug('> Using response from cached request')

        return response.status_code == 200
