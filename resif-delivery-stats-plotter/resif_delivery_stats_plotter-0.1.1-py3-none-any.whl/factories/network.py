# encoding: utf8
import logging
import arrow
from datetime import date
from obspy.clients.fdsn import Client
from obspy.clients.fdsn.header import FDSNNoDataException, FDSNException
from .station import StationFactory
from .enums import EnumObspyLevel
from ..errors import NoDataError, ApiError
from ..models.network import Network

logger = logging.getLogger(__name__)


class NetworkFactory:
    """
    Factory to builds Network objects from an ObsPy instance
    """

    @classmethod
    def from_obspy(cls, obspy_network, level, channel_year=None):
        """
        Create a Network object from an ObsPy instance

        :param obspy_network: The ObsPy instance
        :param level: The ObsPy query level
        :param channel_year: The year to filter opened channels
        :return: A Network initialized object
        :rtype: Network
        """
        logger.debug('NetworkFactory.from_obspy(%s, %s, %s)' % (obspy_network.code, level, channel_year))
        network = Network(
            code=obspy_network.code,
            start_date=obspy_network.start_date,
            end_date=obspy_network.end_date,
        )

        if level in (EnumObspyLevel.station, EnumObspyLevel.channel):
            for obspy_station in obspy_network.stations:
                network.add_station(StationFactory.from_obspy(obspy_station, level, channel_year, obspy_network.code))

        return network

    @classmethod
    def factory(cls, code_network, level=EnumObspyLevel.station, channel=None, channel_year=None): #FIXME: '?HZ,?NZ'
        """
        Gets a Network object from its code

        :param code_network: The code of the network to get
        :param level: The ObsPy query level (default='station')
        :param channel: The channel code to filter
        :param channel_year: The year to filter opened channels
        :return: A Network initialized object
        :rtype: Network
        """
        logger.debug('NetworkFactory.factory(%s, %s, %s, %s)' % (code_network, level, channel, channel_year))
        try:
            params = {
                'network': code_network,
                'level': level,
                'channel': channel,
            }

            inventory = Client('RESIF').get_stations(**params)
            return cls.from_obspy(inventory[0], level, channel_year)
        except FDSNNoDataException:
            logger.warning("Network %s not found" % code_network)
            raise NoDataError()
        except FDSNException as e:
            raise ApiError(e)

    @classmethod
    def list(cls, level=EnumObspyLevel.network, channel=None, year=None, month=None):
        """
        List the available networks from ObsPy

        :param level: The ObsPy query level (default='network')
        :param channel: The channel code to filter
        :param year: The year to filter opened networks
        :param month: The month to filter opened networks
        :return: The list the available networks from ObsPy
        :rtype: list
        """
        logger.debug('NetworkFactory.list(%s, %s, %s, %s)' % (level, channel, year, month))
        try:
            params = {
                'level': level,
                'channel': channel,
            }

            if year and month:
                date_start = date(year, month or 1, 1)
                date_end = arrow.get(date_start).shift(months=1).shift(days=-1).format('YYYY-MM-DD')
                params['starttime'] = date_start
                params['endtime'] = date_end
            elif year:
                params['starttime'] = date(year, 1, 1)
                params['endtime'] = date(year, 12, 31)

            networks = []
            for item in Client('RESIF').get_stations(**params):
                networks.append(cls.from_obspy(item, level))
            return networks

        except FDSNNoDataException:
            logger.warning("No network found")
            raise NoDataError()
        except FDSNException as e:
            raise ApiError(e)
