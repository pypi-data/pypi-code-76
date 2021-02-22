#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Mon Jan 21 11:23:24 CET 2019 -*-
# -*- copyright: GH/IPHC 2019 -*-
# -*- file: interp -*-
# -*- purpose: -*-

'''
Data unpacker fo ADC events

The return dictionnary  as the following keys:
 - dt
 - value
 - saturated
 - pileup
'''

import struct
_the_61_unpacker = struct.Struct("<LL")

alias = 61
type_ = 'adc_event'


def unpack(rawdata, *w, **kw):
    '''unpack adc event data'''
    high, low = _the_61_unpacker.unpack(rawdata)
    measure = low & 0xFFFFFC00 >> 10
    delta_t = high >> 7
    saturated = (low & 0x40000000) >> 30
    pileup = (low & 0x80000000) >> 31
    return {'dt': delta_t,
            'value': measure,
            'saturated': saturated,
            'pileup': pileup}
