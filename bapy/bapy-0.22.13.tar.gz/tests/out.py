#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bapy import icc as ic

from test_caller import *
ic.enabled = True

ic(test_caller())

if __name__ == '__main__':
    pass

