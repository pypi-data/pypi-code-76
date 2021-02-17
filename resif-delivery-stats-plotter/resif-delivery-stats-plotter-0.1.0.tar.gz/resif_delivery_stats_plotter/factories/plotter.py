# encoding: utf8
import logging
from ..services.plotters.png import ServicePlotterPNG
#from ..services.plotters.html import ServicePlotterHTML

logger = logging.getLogger(__name__)


class ServicePlotterFactory:
    """
    Factory to builds ServicePlotter objects
    """

    FORMAT_PNG = 'png'
    FORMAT_HTML = 'html'

    @classmethod
    def factory(cls, plot_format):
        """
        Created a ServicePlotter object

        :param plot_format: The plotting format
        :return: A ServicePlotter initialized object
        :rtype: ServicePlotter
        """
        logger.debug('ServicePlotterFactory.factory(%s)' % plot_format)
        if plot_format == cls.FORMAT_PNG:
            return ServicePlotterPNG
        #elif plot_format == cls.FORMAT_HTML:
        #    return ServicePlotterHTML
        else:
            raise Exception("Format '%s' is not supported by any plotter" % plot_format)
