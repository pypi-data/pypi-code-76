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
Battery monitor and action segment
'''


import typing
import psutil
from ..common import shell
from .classes import BarSeg


EMOJIS = {
    "bat_100": '\uf240',
    "bat_75":  '\uf240',
    "bat_50":  '\uf242',
    "bat_25":  '\uf243',
    "bat_0":   '\uf244',

}


class BatSeg(BarSeg):
    '''
    Battery segment,
    '''

    def _bat_act(self, conn: bool, fill: float, mem: int) -> int:
        '''
        Emergency Actions.

        Args:
            conn: charger connected?
            fill: battery charge fill percentage
            mem: count memory of warning flash notifications

        Returns:
            updated mem

        Notifies:
            ``notify`` emergency multiple times and suspends if critical

        '''
        if conn:
            if fill > 99 and mem < 5:
                mem += 1
                # Send only 5 notifications
                shell.notify('Battery_charged')
        else:
            mem = 0
            if fill < 20:
                shell.notify('Battery Too Low', timeout=0,
                             send_args=('-u', 'critical'))
            elif fill < 10:
                shell.notify('Battery Too Low Suspending Session...',
                             timeout=0, send_args=('-u', 'critical'))
            elif fill < 5:
                shell.process_comm('systemctl', 'suspend',
                                   timeout=-1, fail=False)
        return mem

    def call_me(self, mem: int = None) -> typing.Dict[str, str]:
        '''
        Create Battery summary string

        Args:
            mem: int = count memory of warning flash notifications

        Returns:
            dict to update ``BarSeg`` properties

        '''
        color = None
        sym_pango = ['', '']
        bat_probe = psutil.sensors_battery()
        if not bat_probe:
            return {'symbol': EMOJIS['bat_0'], 'vis': False}
        bat_fill = bat_probe.percent
        bat_conn = bat_probe.power_plugged
        if bat_conn:
            sym_pango = ['<span foreground="#7fffffff">', '</span>']
        # Action
        mem = self._bat_act(conn=bat_conn, fill=bat_fill, mem=mem)
        # returns
        if bat_fill >= 100:
            sym, val, color = EMOJIS['bat_100'], "100", "#7fffffff"
        elif bat_fill > 75:
            sym, val, color = EMOJIS['bat_75'], f"{bat_fill:.2f}", "#ffff7fff"
        elif bat_fill > 50:
            sym, val, color = EMOJIS['bat_50'], f"{bat_fill:.2f}", "#ffaf7fff"
        elif bat_fill > 25:
            sym, val, color = EMOJIS['bat_25'], f"{bat_fill:.2f}", "#ff7f7fff"
        else:
            sym, val, color = EMOJIS['bat_0'], f"{bat_fill:.2f}", "#ff5f5fff"
        sym = sym_pango[0] + sym + sym_pango[1]
        return {'symbol': sym, 'magnitude': val, 'mem': mem, 'color': color}


BATTERY = BatSeg(name="battery",
                 symbol=EMOJIS['bat_0'],
                 units="%",
                 mem=0,
                 pango=True)
'''
battery segment instance
'''
BATTERY.set_proto(markup='pango')
