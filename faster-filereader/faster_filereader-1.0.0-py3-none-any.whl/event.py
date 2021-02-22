#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Tue Jul 24 10:08:42 CEST 2018 -*-
# -*- copyright: GH/IPHC 2018 -*-
# -*- file: event.py -*-
# -*- purpose: -*-

'''
Faster Event class

In addition, the unpackers for the data are imported here.
You should not use the unpackers outside of here!
'''

# faster modules (from within module directory)
import faster.filereader
import faster.const

import faster.dataunpackers
from faster.dataunpackers import *

unpackers = {int(up[5:]): faster.dataunpackers.__dict__.get(up).unpack
             for up in list(filter(lambda x: x.startswith('type'),
                                   dir(faster.dataunpackers)))}
type_aliases = {int(up[5:]): faster.dataunpackers.__dict__.get(up).type_
                for up in list(filter(lambda x: x.startswith('type'),
                                      dir(faster.dataunpackers)))}


def _multiplier(x: float = 1., y: float = 1.) -> float:
    'Just a multiplying function to speed up exectuion via a map'
    return x * y


class Event:
    '''
Faster event class

The Event object is normally instantiated from faster.FileReader.__next__. There is no reason why you would create one yourself.

The Event object has several attributes:
- Directly derived from the event header:
   type_alias : a number indicating the type alias
   clock      : an array of integer containning the clock information (timestamp)
   label      : an integer containing the event label
   load_size  : the size in bytes of the raw data
   raw data   : the raw (i.e. byte) data

- 3 more attributes are accessible and interpreted "just-in-time" for better perfomance:
   type       : a string representing the even type, the correspondance with a type_alias is defined within the dataunpacker file
   time       : the computed timestamp (without the tick interval multiplier)
   data       : a *dictionnary* containning the unpacked data (by the unpackers).


An Event object can be converted to a string with `__repr__` which returns a formated string according to "<{Event.type}({Event.type_alias}), CLOCK={Event.time}, LABEL={Event.label}, LOAD_SIZE={Event.load_size}, DATA={Event.data}>"

An additionnal _repr_head() method returns a slightly different string: "<{Event.type}({Event.type_alias}), CLOCK={Event.time}, LABEL={Event.label}, LOAD_SIZE={Event.load_size}>"

Finally, the Event object implements a dict() method that returns a full dictionnary. It is similar to vars(Event) but first make sure that the time, type, and data are interpreted.
'''
    def __init__(self,
                 header,
                 data):
        '''
        Initialize the event
        '''
        self.type_alias = header['type_alias']
        # self.rawheader = header['rawheader']
        # self.type = 'unknown'
        # self.magic = header['magic']
        # self.time = just in time
        self.clock = header['clock']
        self.label = header['label']
        self.load_size = header['load_size']
        # self.data = {}
        self.rawdata = data
        pass
    # end of __init__

    def __del__(self):
        'Cleanning up'
        del self.clock
        del self.type_alias
        del self.label
        del self.load_size
        del self.rawdata

    def __getattr__(self, attr):
        ''' Used to get Just-In-Time interpreted attributes '''
        return getattr(self, f"_get_{attr}",
                       "_get_nothing")()

    def _get_type(self):
        'JIT interpretation of `type` and return'
        self.type = type_aliases.get(self.type_alias,
                                     type_aliases[0])
        return self.type

    def _get_time(self):
        'JIT interpretation of `time` and return'
        self.time = sum(map(_multiplier,
                            self.clock,
                            faster.const.clock_multipliers))
        return self.time

    def _get_data(self):
        '''return the unpacked data, and store it in self.data'''
        try:
            self.data = unpackers.get(self.type_alias,
                                      unpackers[0])(self.rawdata)
        except Exception:
            self.data = {'error': True,
                         'error_cause': "generic fail at unpacking"}
        return self.data

    def _get_nothing(self):
        'when wrong attribute is called'
        raise AttributeError

    def dict(self) -> dict:
        '''returns a full dictionnary of the event'''
        # first, make sure everything is interpreted
        str(self)
        # then use vars
        return vars(self)

    def _repr_head(self):
        'repr like function that returns only the head'
        return f"<{self.type}, CLOCK={self.clock}, LABEL={self.label}, LOAD_SIZE={self.load_size}>"

    def __repr__(self):
        'String representation of the event'
        return f"<{self.type}({self.type_alias}), CLOCK={self.time}, LABEL={self.label}, LOAD_SIZE={self.load_size}, DATA={self.data}>"
