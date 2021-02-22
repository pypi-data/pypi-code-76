#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Mon Jan 21 11:23:24 CET 2019 -*-
# -*- copyright: GH/IPHC 2019 -*-
# -*- file: interp -*-
# -*- purpose: -*-

'''
Data unpacker fo Trapezoid events

The return dictionnary  as the following keys:
 - dt
 - value
 - saturated
 - sat_cpz
 - pileup
'''

import struct

_the_62_unpacker = struct.Struct("<L")

alias = 62
type_ = 'trapez_event'


def unpack(rawdata, *w, **kw):
    '''unpack trapez event'''
    try:
        word = _the_62_unpacker.unpack(rawdata)[0]
        measure = word & 0x007FFFFF
        saturated = (word & 0x40000000) >> 30
        pileup = (word & 0x20000000) >> 29
        tdc = (word & 0x1f800000) >> 25
        sat_cpz = (word & 0x80000000) >> 31
        return {'value': measure,
                'tdc': tdc,
                'saturated': saturated,
                'sat_cpz': sat_cpz,
                'pileup': pileup}
    except Exception as inst:
        return {'error': True,
                'error_cause': inst}
