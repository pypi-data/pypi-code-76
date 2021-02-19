#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys

def is_debug_mode():
    debugging = False

    gettrace = getattr(sys, 'gettrace', None)
    if gettrace is not None and gettrace():
        debugging = True

    return debugging