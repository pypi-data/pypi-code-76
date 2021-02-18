#!/usr/bin/env python3
# -*- coding:utf-8; mode:python -*-
#
# Copyright 2020-2021 Pradyumna Paranjape
# This file is part of ppsi.
#
# ppsi is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ppsi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with ppsi.  If not, see <https://www.gnu.org/licenses/>.
#
'''
Load yaml configuration file(s), temp storage folder

Load {action: '--flag', ...} for all available menus
Determine a root directory for temporary storage and log files
'''


import os
import typing
from pathlib import Path
import yaml
from .sway_api import sway_nag


def get_defaults() -> typing.Tuple[str, dict]:
    '''
    Returns:
        swayroot: Confirmed existing Path for sway files
        config: dictionary of default config fetched from default locations

    get default values
    '''
    swayroot = '.'
    config = {}
    def_loc = [
        [os.environ.get('XDG_CONFIG_HOME', None), 'sway'],  # Good practice
        [os.environ.get('HOME', None), '.config', 'sway', ],  # The same thing
        [os.path.join(os.path.dirname(__file__)), 'config'],  # Shipped default
    ]
    for location in def_loc:
        if location[0] is not None:
            swayroot = Path(location[0]).joinpath(*location[1:])
            if swayroot.is_dir():
                break

    # default config
    for location in def_loc:
        if location[0] is not None:
            config = Path(location[0]).joinpath(*location[1:], 'ppsi.yml')
            if config.exists():
                break
    return swayroot, config


def read_config(custom_conf: str = None,
                swayroot: str = None) -> typing.Tuple[Path, dict]:
    '''
    Read ppsi configuration from supplied yml file or default
    Define swayroot to store log files.

    Args:
        custom_conf: custom path of config file ppsi.yml
        swayroot: custom path of root directory to store sway data

    Returns:
        swayroot, config referenced by ``menu``
    '''
    # default locations
    defroot, defconfig = get_defaults()
    if swayroot is None:
        swayroot = defroot
    if custom_conf is None:
        root_path = Path(swayroot).joinpath("ppsi.yml")
        if root_path.exists():
            custom_conf = root_path
    if custom_conf is None:
        custom_conf = defconfig
    with open(custom_conf, "r") as config_h:
        try:
            config = yaml.safe_load(config_h)
        except (FileNotFoundError, yaml.composer.ComposerError) as err:
            sway_nag(msg=err, error=True)
    return Path(swayroot).resolve(), config
