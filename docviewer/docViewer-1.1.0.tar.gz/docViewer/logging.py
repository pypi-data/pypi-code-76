import logging

formatter = logging.Formatter(
    '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')

ch = logging.StreamHandler()
ch.setFormatter(formatter)

logger = logging.getLogger('docViewer')
logger.addHandler(ch)


def set_logging_level(level):
    logger.setLevel(level)
    ch.setLevel(level)


set_logging_level(logging.WARNING)
