import logging

from .train import train_is
from .pilot import pilot
from .trace import trace


_logger = logging.getLogger("pyispace")

if not logging.root.handlers:
    _logger.setLevel(logging.DEBUG)
    if len(_logger.handlers) == 0:
        handler = logging.StreamHandler()
        _logger.addHandler(handler)
