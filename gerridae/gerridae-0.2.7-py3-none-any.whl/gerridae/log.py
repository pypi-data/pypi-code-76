"""gerridae log"""
import logging


def get_logger(name="gerridae"):
    logger_format = "[%(asctime)s] %(levelname)s [%(name)s] %(message)s"

    logging.basicConfig(
        format=logger_format, level=logging.INFO, datefmt="%Y:%m:%d %H:%M:%S"
    )

    return logging.getLogger(name)
