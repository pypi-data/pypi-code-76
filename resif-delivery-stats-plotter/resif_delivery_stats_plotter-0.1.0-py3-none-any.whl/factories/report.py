# encoding: utf8
import logging
from .network import NetworkFactory
from ..models.report import Report

logger = logging.getLogger(__name__)


class ReportFactory:
    """
    Factory to builds Report objects
    """

    @classmethod
    def factory(cls, year, code_network):
        """
        Created a Report object

        :param year: The year targeted by the report
        :param code_network: The code of the network targeted by the report
        :return: A Report initialized object
        :rtype: Report
        """
        logger.debug('ReportFactory.factory(%s, %s)' % (year, code_network))
        return Report(year=year, network=NetworkFactory.factory(code_network, channel_year=year))
