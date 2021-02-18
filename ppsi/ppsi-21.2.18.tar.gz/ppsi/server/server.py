#!/usr/bin/env python3
# -*- coding: utf-8; mode: python -*-
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
socket -> ppsid server communications

ppsi servers functions to listen and
decode request/subcommands from unix socket
'''


import os
import sys
import threading
import socket
import psutil
import json
from psprint import print
from ..common import defined
from .commands import CMD
from .event_watcher import open_pipe, EventLogger


def read_json_bytes(pipe: socket) -> dict:
    '''
    kwargs:
        pipe: socket = socket throught which json object arrives

    Returns:
        dict interpreted from incomming json

    Read stream from pipe with handshakes with client
    '''
    pipe.send(defined.COMM['OK'])  # send me size of json bytes
    in_bytes = pipe.recv(defined.HEAD_SIZE)
    if not in_bytes:
        pass
    stream_len = int(in_bytes.decode(defined.CODING))
    pipe.send(defined.COMM['OK'])  # I am ready to accept stream
    json_bytes = pipe.recv(stream_len)
    pipe.send(defined.COMM['OK'])
    return json.loads(json_bytes.decode(defined.CODING))


def handle_cmd(pipe: socket, logger: EventLogger) -> None:
    '''
    kwargs:
        pipe: socket = socket through which client communications arrive
        logger: EventLogger = container object holding logger objects

    Returns:
        None

    Talks to each client (called by threading module)
    '''
    connected = True
    kwargs = {}
    while connected:
        in_bytes = pipe.recv(defined.INST_SIZE)
        if not in_bytes:
            pass
        comm = int.from_bytes(in_bytes, 'big')
        if comm < 0x10:
            # socket communication
            if in_bytes == defined.COMM['ACCEPT']:
                kwargs.update(read_json_bytes(pipe)),
            elif in_bytes == defined.COMM['BYE']:
                connected = False
            elif in_bytes == defined.COMM['EXIT']:
                print('Terminate Server Manually', mark='act')
                pipe.send(defined.COMM['BYE'])
                connected = False
            elif in_bytes == defined.COMM['FAULT']:
                print("Client sent fault, it shouldn't", mark='warn')
                pipe.send(defined.COMM['FAULT'])
            elif in_bytes == defined.COMM['OK']:
                pipe.send(defined.COMM['OK'])
            else:
                print("Bad communication code. This reflects a fault",
                      mark='warn')
                pipe.send(defined.COMM['FAULT'])
        else:
            # ppsi command
            err = CMD[comm & 0xF0](subcmd=comm & 0x0F, **kwargs)
            logger.event_registry(comm=comm)
            if err:
                pipe.send(defined.COMM['FAULT'])
            else:
                pipe.send(defined.COMM['OK'])
    pipe.close()


def manage_socket():
    '''
    If socket file exists, check if ppsid server is running
    If not running, rename socket as .last_session (overwriting target)

    Returns:
        True: if socket can be made available
        False: If Server is running
    '''
    # check if ppsid another is running
    count_daemons = 0
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if 'ppsid' in proc.name().lower():
                count_daemons += 1
        except (psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess):
            pass
    if count_daemons > 1:
        # discounting THIS daemon
        print("Server is already running", mark='err')
        return True
    defined.SOCK_PATH.replace(str(defined.SOCK_PATH) + ".last_session")
    return False


def start_srv():
    '''
    Server that listens to unix socket and handles encoded client requests
    Spawns threads of separate client communications
    '''
    server = socket.socket(family=socket.AF_UNIX, type=socket.SOCK_STREAM)
    wob = open_pipe()
    logger = EventLogger(wob=wob)
    try:
        server.bind(str(defined.SOCK_PATH))
    except OSError:
        if manage_socket():
            return
        server.bind(str(defined.SOCK_PATH))
    print(f'{defined.SOCK_PATH}', pref='listen', pref_color='lg')
    try:
        server.listen()
        while not server._closed:
            pipe, _ = server.accept()
            thread = threading.Thread(target=handle_cmd, args=(pipe, logger))
            thread.start()
    except KeyboardInterrupt:
        pass
    logger.wob.kill()
    os.remove(defined.SOCK_PATH)
    sys.exit(0)
