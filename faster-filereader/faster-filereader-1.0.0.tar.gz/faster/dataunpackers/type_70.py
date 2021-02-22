#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Mon Jan 21 11:23:24 CET 2019 -*-
# -*- copyright: GH/IPHC 2019 -*-
# -*- file: interp -*-
# -*- purpose: -*-

'''
Data unpacker for ADC scaler

The return dictionnary as the following keys:
 - calc
 - sent
 - trig
(or 'error')
'''

import struct
_the_70_unpacker = struct.Struct("<LLL")

alias = 70
type_ = 'adc_scaler'


def unpack(rawdata, *w, **kw):
    '''unpack counter'''
    try:
        calc, sent, trig = _the_70_unpacker.unpack(rawdata)
        return {'calc': calc, 'sent': sent, 'trig': trig}
    except Exception as inst:
        return {'error': True,
                'error_cause': inst}
