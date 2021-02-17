# encoding: utf8
import os
import logging
from .. import ServiceAbstract

logger = logging.getLogger(__name__)


class ServiceReportBuilderAbstract(ServiceAbstract):
    """
    Base class of report builders
    """

    @classmethod
    def build(cls, report):
        return NotImplemented

    @staticmethod
    def output_dir(report, create=False):
        """
        Builds, and creates, an output path for a report
        :param report: The report object
        :param create: Enables the creation of the folders tree if needed
        :return: The generated output path
        :rtype: str
        """
        logger.debug('ServiceReportBuilderAbstract.output_dir(%s, %s)' % (report, create))
        d = os.path.abspath(os.path.join('output', report.network.code, '%s' % report.year))

        if create:
            logger.debug('If needed, creating directory %s' % d)
            os.makedirs(d, exist_ok=True)

        return d
