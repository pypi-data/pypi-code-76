"""Minecraft Runner - A python script for working with servers.

This module provides pytest configuration, like fixtures and definitions.
"""

import os
import pytest


@pytest.fixture()
def omnia_config() -> dict:
    """Write an omnia configuration to $PWD and yield the config dict.

    Cleans up the configuration file after the test returns.
    """
    omnia_config = {
        'registry': 'harbor.jharmison.com',
        'namespace': 'minecraft',
        'repository': 'ftb',
        'tag': 'omnia',
        'port': 25565,
        'eula_accepted': 'yes',
        'ram_start_gb': 1,
        'ram_max_gb': 4
    }
    with open('mc.cfg', 'w') as f:
        f.write('[ftb-omnia]\n')
        [f.write(f'{key} = {omnia_config[key]}\n') for key in omnia_config]

    yield omnia_config

    os.remove('mc.cfg')
