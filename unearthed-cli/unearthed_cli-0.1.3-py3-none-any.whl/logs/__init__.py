"""Unearthed Logging."""
import os
import logging

logger = logging.getLogger("unearthed")

# enable DEBUG level logging if the UNEARTHED_CLI_DEBUG environment variable
# has been set (to any value)
if os.getenv("UNEARTHED_DEBUG") is not None:
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    format = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
    ch.setFormatter(logging.Formatter(format))
    logger.addHandler(ch)
    # logger.debug('logging initialized')
