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
(WIFI)Internet-monitoring segments
'''


import os
import typing
import psutil
from ..common import shell
from ..server.wificonnect import refresh_wifi
from .classes import BarSeg


NETCHECK = os.path.join(os.path.dirname(__file__), 'shell_dep',
                        'netcheck.sh')


class IpAddrSeg(BarSeg):
    '''
    ip address segment
    '''
    def call_me(self, _=None) -> typing.Dict[str, str]:
        '''
        Create IP ADDRESS string.

        Args:
            all are ignored.

        Returns:
            dictionary to update segment attributes
'''
        color = 0x777777
        stdout = shell.process_comm('bash', NETCHECK, fail=False)
        # print("NET_STATUS:", stdout, stderr)
        if stdout is None:
            return {'vis': False}
        addr = stdout.split("\t")[0]
        net_type = int(stdout.split("\t")[2])
        if net_type & 8:
            # internet connected
            color += 0x007f00  # #007f00
        elif net_type & 4:
            # intranet connected
            color += 0x7f7f00  # #7f7f00
        else:
            color += 0x7f0000  # #7f0000
        if net_type & 2:
            # On home network
            color += 0x00007f  # #00007f  #007f7f  #7f7f7f #7f007f
        elif net_type & 1:
            color += 0x00003f  # #00003f  #007f3f  #7f7f3f #7f003f
        if addr.split(".")[:2] == ["192", "168"]:
            return {'magnitude': ".".join(addr.split(".")[2:]),
                    'color': f"#{hex(color)[2:]}"}
        return {'magnitude': addr}

    def callback(self, _):
        '''
        Update wifi connection, refresh
        '''
        pid = os.fork()
        if pid == 0:
            # child
            refresh_wifi()
            self.update()


class NetSpeedSeg(BarSeg):
    '''
    Net speed segment
    '''
    def call_me(self, mem=None) -> typing.Dict[str, str]:
        '''
        Total internet Speed

        Args:
            mem: memory data held between subsequent calls

        Returns:
            dictionary to update segment attributes
        '''
        net_stats = psutil.net_io_counters()
        if not net_stats:
            return {'mem': mem}
        down_l = net_stats.bytes_recv / 1048576
        up_l = net_stats.bytes_sent / 1048576
        diff = (down_l - mem[1])/mem[0], (up_l - mem[2])/mem[0]
        return {'magnitude': f"{diff[0]:.2f}/{diff[1]:.2f}",
                'mem': [mem[0], down_l, up_l]}


IP_ADDR = IpAddrSeg(name="ip", symbol=chr(0x1f4f6), units="")
'''ip address segment instance'''

NETSPEED = NetSpeedSeg(name="netspeed", symbol='\u21f5\u25BC',
                       units='\u25B2MB/s')
'''netspeed segment instance'''
