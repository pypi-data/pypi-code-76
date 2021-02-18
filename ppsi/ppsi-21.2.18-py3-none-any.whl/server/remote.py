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
Call remote commands through ssh/[waypipe]

Interactive username, server, interface, application
that is temporarily remembered till reboot.

TODO: Offer ossify temporary information.

'''


import os
from pathlib import Path
import yaml
import typing
from launcher_menus import menu
from . import CONFIG
from ..common import shell


def handle_tmp_cfg() -> typing.Tuple[str, dict]:
    '''
    look for temporary configuration file to store learnt remote addresses,
    user-names and graphical applications for the session

    Returns:
        location of temporary library
        configuration from temporary library
    '''
    data = {}
    uid = os.environ.get('UID')
    if uid is None:
        # uid couldn't be guessed use temporary directory
        basepath = Path("/tmp")
    else:
        # uid is known
        # try for hard path
        basepath = Path('/run').joinpath('user', str(uid))
    xdg_run: Path = Path(os.environ.get('XDG_RUNTIME_DIR', str(basepath)))
    tmp_cfg = xdg_run.joinpath(
        'sway',
        'ppsi',
        'remote.yml',
    )
    if tmp_cfg.exists():
        with open(tmp_cfg, 'r') as config_h:
            data = yaml.safe_load(config_h)
        if not data:
            data = {}
    return tmp_cfg, data


TMP_CFG, DATA = handle_tmp_cfg()


def add_id(identity: str, new: str = 'user') -> None:
    '''
    Add identity to temporary library.
    This library is maintained in yml format.
    This library gets cleared after system reboot.

    Args:
        identity: new object identity
        new: type of object {'user','host','app'}

    Returns:
        ``None``

    '''
    if not TMP_CFG.exists():
        TMP_CFG.parents[0].mkdir(exist_ok=True)
    if 'remote' not in DATA:
        DATA['remote'] = {'hosts': [], 'users': []}
    if 'apps' not in DATA:
        DATA['apps'] = []
    if new == 'user':
        DATA['remote']['users'].append(identity)
    elif new == 'host':
        DATA['remote']['hosts'].append(identity)
    elif new == 'app':
        DATA['apps'].append(identity)
    with open(TMP_CFG, 'w') as config_h:
        yaml.safe_dump(DATA, config_h)


def which_remote() -> typing.Tuple[str]:
    '''
    Fetch desired remote session details using ``menu``

    Returns:
        username
        host
    '''
    # default config
    known_users: typing.List[str] = CONFIG['remote']['users']
    known_hosts: typing.List[str] = CONFIG['remote']['hosts']

    # temporary config
    if 'remote' in DATA:
        known_users += DATA['remote']['users']
        known_hosts += DATA['remote']['hosts']

    user = menu(opts=known_users, prompt='user') or os.environ['USER']
    host = menu(opts=known_hosts, prompt='host') or 'localhost'
    if user == os.environ['USER'] and host == 'localhost':
        # mind changed
        return None, None
    if user not in known_users:
        add_id(user)
    if host not in known_hosts:
        add_id(host, new='host')
    return user, host


def graphical() -> bool:
    '''
    Get remote interface type: Graphical? Default: False

    Returns:
        Whether graphical interface is demanded [experimental]
    '''
    return menu(opts=['No', 'Yes'], prompt='Graphical') == 'Yes'


def remote_app() -> str:
    '''
    Get remote app, also remember it

    Returns:
        Graphical Remote App
    '''
    known_apps = []
    if 'apps' in DATA:
        known_apps += DATA['apps']
    app = menu(opts=known_apps, prompt='application name')
    if app not in known_apps:
        add_id(app, new='app')
    return app


def call_remote(subcmd=None):
    '''
    Call remote ssh and try to set up a connection
    Use menu launcher to learn
    * username
    * host address
    * interface type {GUI,CLI}
    * Application name (if GUI)

    Args:
        all are ignored

    Returns:
        ``None``

    '''
    user, host = which_remote()
    if host is None or user is None:
        return
    cmd = ['--', 'ssh', f'{user}@{host}']
    if graphical():
        app = remote_app()
        if app is not None:
            cmd.insert(0, 'waypipe')
            cmd.append(
                f'env XDG_SESSION_TYPE=wayland nohup {app} 2>&1 1>/dev/null &'
            )
        else:
            cmd.insert(0, os.environ.get('defterm', 'xterm'))
    else:
        cmd.insert(0, os.environ.get('defterm', 'xterm'))
    shell.process_comm(*cmd, p_name='connecting remote', timeout=-1)
