#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#
import os
import configparser
from loguru import logger
import sys
from pinecone.specs.service import Service  # noqa
from pinecone.specs.traffic_router import TrafficRouter  # noqa
from .constants import Config

__all__ = ["init"]

logging_level = os.environ.get('PINECONE_LOGGING', default="ERROR")
logger.remove()
logger.add(sys.stdout, level=logging_level)

__version__ = open(os.path.join(os.path.dirname(__file__), "__version__")).read().strip()


def init(api_key: str = None, host: str = None, environment: str = None, config: str = "~/.pinecone"):
    """Initializes Pinecone client.

    :param api_key: Required if not set in config file or by environment variable ``PINECONE_API_KEY``.
    :param host: Optional. Controller host.
    :param environment: Optional. Deployment environment.
    """
    # Load from config file first
    config_obj = {}
    if not api_key and config:
        full_path = os.path.expanduser(config)
        if os.path.isfile(full_path):
            parser = configparser.ConfigParser()
            parser.read(full_path)
            if "default" in parser.sections():
                config_obj = {**parser["default"]}

    config_obj['api_key'] = api_key or config_obj.get('api_key')
    config_obj['controller_host'] = host or config_obj.get('host')
    config_obj['environment'] = environment or config_obj.get('environment')
    Config.reset(**config_obj)

    if not bool(Config.API_KEY):
        logger.warning("API key is required.")


# Init the config
init()
