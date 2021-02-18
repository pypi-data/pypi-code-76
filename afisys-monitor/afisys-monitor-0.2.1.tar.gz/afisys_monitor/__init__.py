#!/usr/bin/env python
"""
AFiSys Monitor
"""

__version__ = '0.2.1'

import logging as log

from .monitor import Monitor


def _real_main():
    Monitor()
    exit(0)


def main():
    try:
        _real_main()
    except KeyboardInterrupt:
        log.critical('\nERROR: Interrupted by user')
    except Exception as e:
        log.critical('Fatal error: %s' % e)
        exit(1)


def test():
    print('Hello world!')
