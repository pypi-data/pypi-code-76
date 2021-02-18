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
common shell calls functions
'''


import os
import typing
import subprocess


def notify(info: str, timeout: int = 5,
           send_args: typing.Tuple[str] = ()) -> None:
    '''
    Push ``info`` to notify-send for ``timeout`` seconds

    Args:
        info: str = information to notify
        timeout: int = remove notification after seconds. [0 => permament]
        send_args: arguments passed to notify-send command

    Returns:
        None

    '''
    if os.environ.get("READTHEDOCS"):
        # RTD virutal environment
        return None
    icon = os.path.join(os.path.dirname(__file__), 'icon.jpg')
    timeout *= 1000  # miliseconds
    cmd = ['notify-send', '--icon', icon]
    cmd.extend(send_args)
    if timeout > 0:
        cmd += ['-t', f'{timeout}']
    cmd.append(info)
    subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def process_comm(*cmd: str,
                 p_name: str = 'processing',
                 timeout: int = None,
                 fail: bool = True, **kwargs) -> str:
    '''
    Generic process definition and communication

    Args:
        *cmd: list(args) passed to subprocess.Popen as first argument
        p_name: notified as 'Error {p_name}: {stderr}
        timeout: communicatoin timeout. If -1, 'communicate' isn't called
        fail: if False, don't exit on error
        **kwargs: passed on to subprocess.Popen

    Returns:
        ``stdout`` from command's communication
        None if stderr and ``fail`` is ``False``
        ``notify`` message if stderr

    '''
    if os.environ.get("READTHEDOCS"):
        # RTD virutal environment
        return None
    cmd = list(cmd)
    if timeout is not None and timeout < 0:
        process = subprocess.Popen(cmd, **kwargs)  # DONT: *cmd here
        return None
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        **kwargs
    )
    stdout, stderr = process.communicate(timeout=timeout)
    if stderr:
        notify(f'Error {p_name}: {stderr}')
        if fail:
            return None
    return stdout
