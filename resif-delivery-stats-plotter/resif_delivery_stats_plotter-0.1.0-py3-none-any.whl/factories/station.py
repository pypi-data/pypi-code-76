# encoding: utf8
import logging
from ..errors import NoDataError
from ..models.station import Station
from .channel import ChannelFactory
from .enums import EnumObspyLevel

logger = logging.getLogger(__name__)


class StationFactory:
    """
    Factory to builds Station objects from an ObsPy instance of Channel
    """

    @classmethod
    def from_obspy(cls, obspy_station, level, channel_year=None, network_code=None):
        """
        Create a Channel object from an ObsPy instance

        :param obspy_station: The ObsPy instance
        :param level: The ObsPy query level
        :param channel_year: The year to filter opened channels
        :return: A Station initialized object
        :rtype: Station
        """
        logger.debug('StationFactory.from_obspy(%s, %s, %s, %s)' % (obspy_station.code, level, channel_year, network_code))
        station = Station(
            code=obspy_station.code,
            start_date=obspy_station.start_date,
            end_date=obspy_station.end_date,
            latitude=obspy_station.latitude,
            longitude=obspy_station.longitude,
            elevation=obspy_station.elevation,
            network_code=network_code
        )

        if channel_year is not None and network_code is not None:
            try:
                for channel in ChannelFactory.list(network_code, obspy_station.code, year=channel_year):
                    station.add_channel(channel)
            except NoDataError:
                pass
        elif level == EnumObspyLevel.channel:
            for obspy_channel in obspy_station.channels:
                station.add_channel(ChannelFactory.from_obspy(obspy_channel, year=channel_year))

        return station
