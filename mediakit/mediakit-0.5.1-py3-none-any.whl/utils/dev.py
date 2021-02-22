#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from mediakit.utils.regex import ANSI_ESCAPE_CODES_REGEX, sub

def append_to_debug_output(debug_data, end='\n'):
    debug_data_clear_of_colors = sub(
        ANSI_ESCAPE_CODES_REGEX,
        '',
        str(debug_data)
    )

    with open('debug.txt', 'a') as debug:
        debug.write(debug_data_clear_of_colors + end)
