"""Minecraft Runner - A python script for working with servers.

This module provides a mechanism to load configuration from the system.
"""

import os
from configparser import ConfigParser

from .util import get_logger

logger = get_logger()

config_locations = [
    '/etc/mc.cfg',
    os.path.expanduser('~/.config/minecraft-runner/mc.cfg'),
    './mc.cfg'
]
if os.getenv('MINECRAFT_RUNNER_CONF') is not None:
    config_locations.append(os.getenv('MINECRAFT_RUNNER_CONF'))

default_config = {
    'registry': 'harbor.jharmison.com',
    'namespace': 'minecraft',
    'repository': 'ftb',
    'tag': 'revelation',
    'port': 25565,
    'eula_accepted': 'no',
    'ram_start_gb': 8,
    'ram_max_gb': 16
}


def initialize(default_config: dict = default_config,
               config_locations: list = config_locations) -> ConfigParser:
    """Initialize a fresh configuration, reevaluating config_locations."""
    config = ConfigParser()
    config['DEFAULT'] = default_config

    for config_file in config_locations:
        if os.path.exists(config_file):
            logger.info(f'Loading configuration: {config_file}')
            config.read(config_file)
            logger.debug({section: dict(config[section])
                          for section in config.sections()})

    if config.sections() == []:
        logger.info('No configuration found. Loading defaults.')
        config.read_dict({"ftb-revelation": default_config})
        logger.debug(default_config)

    # Build the image section dynamically
    for section in config.sections():
        config[section]['image'] = (
            f"{config[section].get('registry')}/"
            f"{config[section].get('namespace')}/"
            f"{config[section].get('repository')}:"
            f"{config[section].get('tag')}"
        )
        logger.debug(f'{section} image: {config[section]["image"]}')

    return config


config = initialize(default_config, config_locations)
