# encoding: utf8
import os
import logging
from .. import ServiceAbstract

logger = logging.getLogger(__name__)


class ServicePlotterAbstract(ServiceAbstract):
    """
    Base class of plotters
    """

    @staticmethod
    def output_dir(network, year, create=True):
        """
        Builds, and creates, an output path for a network code and a year
        :param network: The network code
        :param year: The year
        :param create: Enables the creation of the folders tree if needed
        :return: The generated output path
        :rtype: str
        """
        logger.debug('ServicePlotterAbstract.output_dir(%s, %s, %s)' % (network, year, create))
        d = os.path.abspath(os.path.join('output', network.code, '%s' % year))

        if create:
            logger.debug('If needed, creating directory %s' % d)
            os.makedirs(d, exist_ok=True)

        return d
