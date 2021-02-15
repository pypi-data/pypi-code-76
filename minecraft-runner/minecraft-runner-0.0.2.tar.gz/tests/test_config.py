"""Minecraft Runner - A python script for working with servers.

This module provides tests for the commun utilities like the logger and shell
functions.
"""

from minecraft_runner.util import get_logger
logger = get_logger(verbosity=0)


def test_default_config():
    """Instantiate a default configuration and verify it."""
    from minecraft_runner.config import config, default_config
    expected_image = ':'.join([
        '/'.join([
            default_config[item]
            for item in ['registry', 'namespace', 'repository']
        ]),
        default_config['tag']
    ])
    logger.debug({section: config[section] for section in config.sections()})
    assert config['ftb-revelation']['image'] == expected_image


def test_modified_config(omnia_config):
    """Instantiate a configuration with a local configuration present."""
    from minecraft_runner.config import initialize
    config = initialize()
    expected_image = ':'.join([
        '/'.join([
            omnia_config[item]
            for item in ['registry', 'namespace', 'repository']
        ]),
        omnia_config['tag']
    ])
    logger.debug({section: config[section] for section in config.sections()})
    assert config['ftb-omnia']['image'] == expected_image
