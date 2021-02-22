import logging
import asyncio

from .adapters.specs.http import *
from .adapters.asynchronous import *
from .commands.action import *
from .commands.download import *
from .core.asynchronous import *
from .core.base import *

fmt = "[%(asctime)s] [%(filename)s: %(lineno)d] [%(levelname)s] => %(message)s"

logging.basicConfig(
    level="INFO", format=fmt,
)
