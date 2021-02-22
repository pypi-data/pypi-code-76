#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Extend PyTado interface to provide more information easily.'''

from PyTado.interface import Tado


class TadoExtended(Tado):
    '''Extends the PyTado interface to provide additional methods.'''

    def getHeatingState(self, zone):
        '''Gets set temperature (centigrade) and heating power (%) for Zone zone.'''

        data = self.getState(zone)
        return {'temperature': data['setting']['temperature']['celsius'],
                'power': data['activityDataPoints']['heatingPower']['percentage']}
    
    def getOpenWindow(self, zone):
        '''Gets open window status for Zone zone.'''

        if self.getState(zone)['openWindow'] is None:
            return False
        else:
            return True
    