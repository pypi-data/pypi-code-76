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
API-like calls for swaymsg, swaynag

Swaymsg calls through subprocess module
'''


from ..common import shell
import subprocess


def sway_nag(msg: str, **kwargs) -> str:
    '''
    Display panic message on top of screen using swaynag

    Args:
        msg: message to sway on swaynag bar
        **kwargs: passed on to subprocess.Popen

    Returns:
        swaynag's stdout
        None if time-out

    '''
    if kwargs.get('error'):
        bg_col = 'ff3f1f'
        color = '00c0e0'
    elif kwargs.get('info'):
        bg_col = '000080'
        color = '7fafff'
    else:
        bg_col = '000000'
        color = '7f7f7f'
    sway_report = ['swaynag', '--background', bg_col, '--text', color,
                   '--message', msg]
    try:
        stdout = shell.process_comm(*sway_report, timeout=5, **kwargs)
    except subprocess.TimeoutExpired:
        return None
    return stdout


def sway_call(*swaycmd: str, **kwargs) -> str:
    '''
    Subprocess opened with swaymsg

    Args:
        *swaycmd: sway command
        **kwargs: passed on to subprocess.Popen

    Returns:
        swaymsg's stdout

    '''
    swaycmd = ['swaymsg'] + list(swaycmd)
    stdout = shell.process_comm(*swaycmd, **kwargs)
    return stdout


def sway_query(*swaycmd: str, **kwargs) -> str:
    '''
    Subprocess opened with swaymsg -t

    Args:
        *swaycmd: query command
    **kwargs: passed on to subprocess.Popen

    Returns:
        swaymsg's stdout

    '''
    swaycmd = ['-t'] + list(swaycmd)
    return sway_call(*swaycmd, **kwargs)


def sway_bind(*swaycmd: str, **kwargs) -> str:
    '''
    Keybindings called with subprocess swaymsg bindsym

    Args:
        *swaycmd: query command
        **kwargs: passed on to subprocess.Popen

    Returns:
        swaymsg's stdout

    '''
    swaycmd = ['bindsym'] + list(swaycmd)
    return sway_call(*swaycmd, **kwargs)


def sway_ws(*swaycmd: str, **kwargs) -> str:
    '''
    Workspace calls with subprocess swaymsg workspace

    Args:
        *swaycmd: query command
        **kwargs: passed on to subprocess.Popen

    Returns:
        swaymsg's stdout

    '''
    swaycmd = ['workspace'] + list(swaycmd)
    return sway_call(*swaycmd, **kwargs)


def sway_assign(*swaycmd: str, **kwargs) -> str:
    '''
    App_id assignments to workspaces called with subprocess swaymsg assign

    Args:
        *swaycmd: query command
        **kwargs: passed on to subprocess.Popen

    Returns:
        swaymsg's stdout

    '''
    swaycmd = ['assign'] + list(swaycmd)
    return sway_call(*swaycmd, **kwargs)
