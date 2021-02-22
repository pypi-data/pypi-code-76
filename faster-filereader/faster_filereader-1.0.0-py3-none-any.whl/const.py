#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Tue Jul 24 10:37:21 CEST 2018 -*-
# -*- copyright: GH/IPHC 2018 -*-
# -*- file: const.py -*-
# -*- purpose: -*-

'''
Constants for faster file reader and unpacker.

The constants of interest for the end user are:
- `max_number_of_events_in_file=180000000` based on a maximum size
    of 2GB per file and minimal size of event 12 bytes.
- `max_adc_amplitude`: the maximum value coded for an ADC event.
- `tick_seconds = 2.0e-9`: the timestamp tick interval, expressed in seconds
- `tick_ns = 2.0`: the timestamp tick vinterval, expressed in nanoseconds
'''

import struct
import math


# Max size of file is 2GB, events are at least 12 bytes long
max_number_of_events_in_file = 180000000

# Max amplitude in ADC data
adc_coding_size = 22
max_adc_amplitude = int(math.pow(2, adc_coding_size - 1))

tick_seconds = 2.0e-9
tick_ns = 2.0

header_byte_size = 12
clock_byte_size = 6
header_fmt = "< B B " + str(clock_byte_size) + "B H H"
header_size = struct.calcsize(header_fmt)
clock_fmt = "<" + str(clock_byte_size) + "B"
clock_multipliers = [1, 256, 65536, 16777216, 4294967296, 1099511627776]
