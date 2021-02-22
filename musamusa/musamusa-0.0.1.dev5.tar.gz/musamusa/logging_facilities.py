# TODO
import datetime
import time

import musamusa.global_logger

def first_log():
    """
    TODO
    """
    musamusa.global_logger.LOGGER.info("{name} v. {version}".format(
        name=musamusa.aboutproject.__projectname__,
        version=musamusa.aboutproject.__version__))
    musamusa.global_logger.LOGGER.info("=== new start === at {timestamp}".format(
        timestamp=datetime.datetime.fromtimestamp(time.time())))
