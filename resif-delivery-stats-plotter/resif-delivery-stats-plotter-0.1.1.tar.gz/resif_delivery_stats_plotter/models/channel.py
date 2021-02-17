# encoding: utf8
from datetimerange import DateTimeRange
from resif_delivery_stats_plotter.services.clients.availabilty import ServiceClientAvailability as service_availability
from resif_delivery_stats_plotter.services.clients.statistics import ServiceClientStatistics as service_stats
from .enums import EnumChannelBand, EnumChannelInstrument


class Channel:
    """
    Defines a channel
    """

    def __init__(self, code=None, location=None):
        self._network_code = None
        self._station_code = None
        self.location = location
        self.code = code
        if code:
            split_code = list(code)
            self._band = split_code[0]
            self._instrument = split_code[1]
            self._orientation = split_code[2]

        self.timeslots = []

    def __repr__(self):
        return "<Channel %s (%i timeslots)>" % (
            self.location_code,
            len(self.timeslots)
        )

    def __lt__(self, other):
        """
        Check if the current channel is 'before' another
        Inspired by the work of Marc Grunberg (https://gitlab.com/eost/qc)

        :param other: An other channel to compare
        """
        if not isinstance(other, Channel):
            raise Exception("Unable to compare a 'Channel' object with '%s'" % type(other))

        def cmp(a, b):
            return (a > b) - (a < b)

        weight_sr = {"M": 9, "R": 8, "U": 7,
                     "V": 6, "L": 5, "B": 4,
                     "S": 3, "E": 2, "H": 1,
                     "C": 0, "D": -1}
        weight_gain = {"N": 2, "L": 1, "H": 0,
                       "V": 3, "D": 4, "T": 5,
                       "X": 6, "M": 7, "A": 8,
                       "W": 9, "E": 10, "K": 11}
        weight_cmp = {"E": 2, "N": 1, "Z": 0,
                      "3": 2, "2": 1, "1": 0.1,
                      "X": 1, "Y": 2,
                      "A": 3, "B": 4, "C": 5, "D": 6,
                      "O": 4, "V": 5, "S": 6}

        # check channel
        for i, w in zip((0, 1, 2), (weight_sr, weight_gain, weight_cmp)):
            try:
                res = cmp(w[self.code[i]], w[other.code[i]])
            except:
                # other code not yet handled, use lexico order only
                res = cmp(self.code[i], other.code[i])
            if res:
                break

        return res

    # CODES
    ####################################################################################################################

    @property
    def has_location(self):
        """
        Checks if the channel has a location

        :rtype: bool
        """
        return self.location is not None and self.location != ''

    @property
    def location_code(self):
        """
        Builds a full code including location if available

        :rtype: str
        """
        if self.has_location:
            return "%s.%s" % (self.location, self.code)
        else:
            return self.code

    @property
    def group_code(self):
        """
        Builds a custom code (without orientation)

        :rtype: str
        """
        return self.custom_code(
            with_location=True,
            with_band=True,
            with_instrument=True,
            with_orientation=False,
        )

    def custom_code(self, with_location=True, with_band=True, with_instrument=True, with_orientation=False):
        """
        Builds a custom code for the current channel

        :param with_location: Includes the location into the generated code
        :param with_band: Includes the band into the generated code
        :param with_instrument: Includes the instrument into the generated code
        :param with_orientation: Includes the orientation into the generated code
        :return: The generated custom code
        :rtype: str
        """
        code = ''
        if with_band:
            code += self._band
        if with_instrument:
            code += self._instrument
        if with_orientation:
            code += self._orientation

        if with_location and self.location:
            if code:
                code = '%s.%s' % (self.location, code)
            else:
                code += self.location

        return code

    @property
    def _instrument_orientation(self):
        """
        Gets the instrument and the orientation of the current channel

        :rtype: str
        """
        return "%s%s" % (self._instrument, self._orientation)

    @property
    def instrument(self):
        """
        Gets the instrument of the current channel

        :rtype: EnumChannelInstrument
        """
        return EnumChannelInstrument(self._instrument)

    @property
    def band(self):
        """
        Gets the band of the current channel

        :rtype: EnumChannelBand
        """
        return EnumChannelBand(self._band)

    # TIMESLOTS
    ####################################################################################################################

    def add_timeslot(self, timeslot):
        """
        Adds a timeslot to the current channel

        :param timeslot: The simeslot to add
        """
        self.timeslots.append(timeslot)

    def is_open(self, year):
        """
        Checks if the channel has been opened during a year

        :param year: The year to check
        :rtype: bool
        """
        for timeslot in self.timeslots:
            if timeslot.is_open(year):
                return True

        return False

    def get_timeslots(self, year):
        """
        Gets the timeslots of a year

        :param year: The year to filter
        :return: The list of timeslots opened during a specific year
        :rtype: list
        """
        timeslots = []

        for timeslot in self.timeslots:
            if timeslot.is_open(year):
                timeslots.append(timeslot)

        return timeslots

    def get_best_timeslot(self, year):
        """
        Gets the best timeslot of a year

        :param year: The year to filter
        :return: The timeslots with the longest opened period during a specific year
        :rtype: ChannelTimeslot
        """
        best_timeslot = None

        for timeslot in self.timeslots:
            if timeslot.is_open(year) and (best_timeslot is None or timeslot.date_range_intersection(year).timedelta > best_timeslot.date_range_intersection(year).timedelta):
                best_timeslot = timeslot

        return best_timeslot

    # STATISTICS
    ####################################################################################################################

    def requests(self, year=None, month=None, country=None, media=None):
        """
        Get the requests number for the current channel

        :param year: The year to filter the requests
        :param month: The month to filter the requests
        :param country: The country to filter the requests
        :param media: The media to filter the requests
        :return: The requests number
        :rtype: int
        """
        return service_stats.requests(network=self._network_code, station=self._station_code, location=self.location, channel=self.code, year=year, month=month, country=country, media=media)

    def requests_by_country(self, year=None, month=None, country=None, media=None):
        """
        Get the requests number for each country, for the current channel

        :param year: The year to filter the requests
        :param month: The month to filter the requests
        :param country: The country to filter the requests
        :param media: The media to filter the requests
        :return: The requests number
        :rtype: int
        """
        return service_stats.requests_by_country(network=self._network_code, station=self._station_code, location=self.location, channel=self.code, year=year, month=month, country=country, media=media)

    def clients(self, year=None, month=None, country=None, media=None):
        """
        Get the clients number for each country, for the current channel

        :param year: The year to filter the clients
        :param month: The month to filter the clients
        :param country: The country to filter the clients
        :param media: The media to filter the clients
        :return: The clients number
        :rtype: int
        """
        return service_stats.clients(network=self._network_code, station=self._station_code, location=self.location, channel=self.code, year=year, month=month, country=country, media=media)

    def clients_by_country(self, year=None, month=None, country=None, media=None):
        """
        Gets the amount of data send for the current channel

        :param year: The year to filter the stats
        :param month: The month to filter the stats
        :param country: The country to filter the stats
        :param media: The media to filter the stats
        :param unit: The unit to convert the result into (default: 'Bytes')
        :return: The amount of data send
        :rtype: int
        """
        return service_stats.clients_by_country(network=self._network_code, station=self._station_code, location=self.location, channel=self.code, year=year, month=month, country=country, media=media)

    def data_send(self, year=None, month=None, country=None, media=None, unit=None):
        """
        Gets the amount of data send by dataselect for the current channel

        :param year: The year to filter the stats
        :param month: The month to filter the stats
        :param country: The country to filter the stats
        :param unit: The unit to convert the result into (default: 'Bytes')
        :return: The amount of data send by dataselect
        :rtype: int
        """
        return service_stats.data_send(network=self._network_code, station=self._station_code, location=self.location, channel=self.code, year=year, month=month, country=country, media=media, unit=unit)

    def data_send_dataselect(self, year=None, month=None, country=None, unit=None):
        """
        Gets the amount of data send by dataselect for the current channel

        :param year: The year to filter the stats
        :param month: The month to filter the stats
        :param country: The country to filter the stats
        :param unit: The unit to convert the result into (default: 'Bytes')
        :return: The amount of data send by dataselect
        :rtype: int
        """
        return self.data_send(year=year, month=month, country=country, media='dataselect', unit=unit)

    def data_send_seedlink(self, year, month=None, country=None, unit=None):
        """
        Gets the amount of data send by seedlink for the current channel

        :param year: The year to filter the stats
        :param month: The month to filter the stats
        :param country: The country to filter the stats
        :param unit: The unit to convert the result into (default: 'Bytes')
        :return: The amount of data send by seedlink
        :rtype: int
        """
        return self.data_send(year=year, month=month, country=country, media='seedlink', unit=unit)

    def data_send_station(self, year, month=None, country=None, unit=None):
        """
        Gets the amount of data send by station WS for the current channel

        :param year: The year to filter the stats
        :param month: The month to filter the stats
        :param country: The country to filter the stats
        :param unit: The unit to convert the result into (default: 'Bytes')
        :return: The amount of data send by station WS
        :rtype: int
        """
        return self.data_send(year=year, month=month, country=country, media='station', unit=unit)

    def availability(self, year, month=None, quality=None):
        """
        Gets the availability periods for the current channel

        :param year: The year to filter the stats
        :param month: The month to filter the stats
        :param quality: The quality to filter the stats
        :return: The amount of data send by station WS
        :rtype: list
        """
        return service_availability.channel(self.code, self.location, self._station_code, self._network_code, year, month, quality)

    def check_availability(self, year, month=None, quality=None):
        """
        Checks the availability periods for the current channel

        :param year: The year to filter the stats
        :param month: The month to filter the stats
        :param quality: The quality to filter the stats
        :return: Boolean flag telling if 'availability' stats are available for this channel
        :rtype: bool
        """
        return service_availability.check_channel(self.code, self.location, self._station_code, self._network_code, year, month, quality)


class ChannelTimeslot:
    """
    Defines a timeslot for a channel
    """

    def __init__(self, start_date, end_date):
        if isinstance(start_date, tuple):
            self._start_date = start_date[0]
        else:
            self._start_date = start_date

        if isinstance(end_date, tuple):
            self._end_date = end_date[0]
        else:
            self._end_date = end_date

    def __repr__(self):
        return "<ChannelTimeslot (%s - %s)>" % (
            self.date_start, self.date_end
        )

    @property
    def date_start(self):
        """
        Gets the open date in ISO format for the current timeslot

        :rtype str
        """
        if self._start_date:
            return self._start_date.isoformat()

    @property
    def date_end(self):
        """
        Gets the close date in ISO format for the current timeslot

        :rtype str
        """
        if self._end_date:
            return self._end_date.isoformat()

    @property
    def date_range_full(self):
        """
        Gets the full date range for the current timeslot

        :rtype DateTimeRange
        """
        return DateTimeRange(self.date_start, self.date_end)

    def date_range_intersection(self, year):
        """
        Gets the intersection date range for the current timeslot with a specific year

        :rtype DateTimeRange
        """
        return self.date_range_full.intersection(DateTimeRange("%i-01-01" % year, "%i-12-31" % year))

    def is_open(self, year):
        """
        Checks if the channel timeslot was during a specific year

        :param year: The year to check
        :rtype: bool
        """
        return self.date_range_full.is_intersection(DateTimeRange("%i-01-01" % year, "%i-12-31" % year))
