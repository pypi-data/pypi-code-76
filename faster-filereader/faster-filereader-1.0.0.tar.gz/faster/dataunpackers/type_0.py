#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Mon Jan 21 11:23:24 CET 2019 -*-
# -*- copyright: GH/IPHC 2019 -*-
# -*- file: interp -*-
# -*- purpose: -*-

'''
Data unpacker for unknown/unsupported data type
'''

alias = 0
type_ = 'unknown type'


def unpack(data, *w, **kw):
    '''always returns an error'''
    return {'error': True,
            'error_cause': "unknown data type"}
