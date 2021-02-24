# encoding: utf8
import logging
from datetime import date
from obspy.clients.fdsn import Client
from obspy.clients.fdsn.header import FDSNNoDataException, FDSNException
from .enums import EnumObspyLevel
from ..errors import NoDataError, ApiError
from ..models.channel import Channel, ChannelTimeslot

logger = logging.getLogger(__name__)


class ChannelFactory:
    """
    Factory to builds Channel objects from an ObsPy instance
    """

    @classmethod
    def from_obspy(cls, obspy_channel, with_timeslot=True, year=None):
        """
        Create a Channel object from an ObsPy instance

        :param obspy_channel: The ObsPy instance
        :param with_timeslot: Creates the first ChannelTimeslot object
        :param year: The year to filter opened timeslots
        :return: A Channel initialized object
        :rtype: Channel
        """
        logger.debug('ChannelFactory.from_obspy(%s, %s, %s)' % (obspy_channel.code, with_timeslot, year))
        channel = Channel(
            code=obspy_channel.code,
            location=obspy_channel.location_code,
        )

        if with_timeslot:
            timeslot = ChannelTimeslotFactory.from_obspy(obspy_channel)
            if year is None or timeslot.is_open(year):
                channel.add_timeslot(timeslot)

        return channel

    @classmethod
    def location_code_from_obspy(cls, obspy_channel):
        """
        Generates a location code from an ObsPy instance

        :param obspy_channel: The ObsPy instance
        :return: The location code of the channel
        :rtype: str
        """
        if hasattr(obspy_channel, 'location_code') and obspy_channel.location_code not in (None, '', 'None'):
            return "%s.%s" % (obspy_channel.location_code, obspy_channel.code)
        else:
            return obspy_channel.code

    @classmethod
    def list(cls, code_network, code_station, level=EnumObspyLevel.channel, year=None):
        """
        Gets a Channel object from its code

        :param code_network: The code of the network to get
        :param code_station: The code of the station to get
        :param level: The ObsPy query level (default='channel')
        :param year: The year to filter opened stations and channels
        :return: A Network initialized object
        :rtype: Network
        """
        logger.debug('ChannelFactory.list(%s, %s, %s, %s)' % (code_network, code_station, level, year))
        try:
            params = {
                'network': code_network,
                'station': code_station,
                'level': level,
            }

            if year:
                params['starttime'] = date(year, 1, 1)
                params['endtime'] = date(year, 12, 31)

            channels = []
            for obspy_network in Client('RESIF').get_stations(**params):
                for obspy_station in obspy_network.stations:
                    for obspy_channel in obspy_station.channels:
                        channel = cls.from_obspy(obspy_channel, year=year)
                        channels.append(channel)
            return channels

        except FDSNNoDataException:
            logger.warning("No channel found for station %s.%s" % (code_network, code_station))
            raise NoDataError()
        except FDSNException as e:
            raise ApiError(e)


class ChannelTimeslotFactory:
    """
    Factory to builds ChannelTimeslot objects from an ObsPy instance of Channel
    """

    @classmethod
    def from_obspy(cls, obspy_channel):
        """
        Create a ChannelTimeslot object from an ObsPy instance

        :param obspy_channel: The ObsPy instance
        :return: A ChannelTimeslot initialized object
        :rtype: ChannelTimeslot
        """
        logger.debug('ChannelTimeslotFactory.from_obspy(<%s, %s, %s>)' % (obspy_channel.code, obspy_channel.start_date, obspy_channel.end_date))
        timeslot = ChannelTimeslot(
            start_date=obspy_channel.start_date,
            end_date=obspy_channel.end_date,
        )
        return timeslot
