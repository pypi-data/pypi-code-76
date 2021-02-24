# encoding: utf8
from resif_delivery_stats_plotter.services.report_builders.html import ServiceReportBuilderHtml
from resif_delivery_stats_plotter.errors import NoDataError
from resif_delivery_stats_plotter.factories.network import NetworkFactory


class Report:
    """
    Defines a report
    """

    FORMAT_HTML = 'html'
    FORMAT_PNG = 'png'

    def __init__(self, year=None, network=None, stations=[]):
        self.year = year
        self.network = network
        self._stations = stations

    @property
    def stations(self):
        """
        Gets the list of stations of the current network

        :return: A collection of stations
        :rtype: list
        """
        if self._stations:
            return self._stations
        elif self.network:
            return self.network.stations

    @stations.setter
    def stations(self, value):
        """
        Sets the list of stations

        :param value: The list of station to set
        """
        self._stations = value

    def build(self, output_format=FORMAT_PNG, unit=None, width=None, height=None, with_plots=True):
        """
        Builds the report

        :param output_format: The output format ('png'|'html')
        :param unit: The unit to use for data plots
        :param width: The width of generated images
        :param height: The height of generated images
        :param with_plots: Include plots
        :return: The output filename of the report
        :rtype: str
        """
        if output_format in (self.FORMAT_HTML, self.FORMAT_PNG):
            try:
                return ServiceReportBuilderHtml.build(self, output_format=output_format, unit=unit, width=width, height=height, with_plots=with_plots)
            except NoDataError:
                # TODO
                raise
        else:
            raise Exception("Format '%s' is not supported by any builder" % output_format)

    @property
    def networks(self):
        """
        Gets the list of available networks

        :return: The  list of available networks
        :rtype: list
        """
        return NetworkFactory.list(year=self.year)
