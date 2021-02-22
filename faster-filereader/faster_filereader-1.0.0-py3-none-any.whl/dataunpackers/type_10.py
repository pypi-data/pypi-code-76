#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Mon Jan 21 11:23:24 CET 2019 -*-
# -*- copyright: GH/IPHC 2019 -*-
# -*- file: interp -*-
# -*- purpose: -*-

'''
Unpacker for group data type

The unpacked data is a dictionnary with the key 'events' containning a tuple of the subevents. Or 'error' = the exception object in case an error occured.
'''
from io import BytesIO as StringBuffer

# faster modules (from within module directory)
import faster.filereader
import faster.event
import faster.const

alias = 10
type_ = 'group'


def unpack(rawdata, *w, **kw):
    '''unpack Group data'''
    # A group is just some generic events...
    data = {'events': ()}
    try:
        the_data = StringBuffer(rawdata)
        head_data = the_data.read(faster.const.header_size)
        events = []
        while head_data:
            header = faster.filereader.FileReader.read_header(head_data)
            evt_data = faster.filereader.FileReader.read_data(the_data, header)
            events.append(faster.event.Event(header, data=evt_data))
            head_data = the_data.read(faster.const.header_size)
        # end while
        data['events'] = tuple(events)
    except Exception as inst:
        data['error'] = True
        data['error_cause'] = inst
    return data
