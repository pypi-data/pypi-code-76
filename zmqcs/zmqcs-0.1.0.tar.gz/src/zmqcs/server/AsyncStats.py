#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" A simple python script

"""
__author__ = 'Otger Ballester'
__copyright__ = 'Copyright 2020'
__date__ = '01/07/2020'
__credits__ = ['Otger Ballester', ]
__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Otger Ballester'
__email__ = 'otger@ifae.es'

from datetime import datetime


class PubStat(object):
    def __init__(self, topic):
        self.topic = topic
        self._timestamps = []
        self._total_pub = 0
        self._last_clean = datetime.utcnow().timestamp()
        self._created = datetime.utcnow().timestamp()

    def pub(self):
        self._total_pub += 1
        now = datetime.utcnow().timestamp()
        self._timestamps.append(now)
        self._clean(now)

    def _clean(self, now):
        if now - self._last_clean > 60:
            self._timestamps = [x for x in self._timestamps if now - x < 3600]
            self._last_clean = now

    @property
    def stats(self):
        now = datetime.utcnow().timestamp()
        self._clean(now)
        return {
            'total_pub': self._total_pub,
            '1min': len([x for x in self._timestamps if now - x < 60]),
            '5min': len([x for x in self._timestamps if now - x < 300]),
            '15min': len([x for x in self._timestamps if now - x < 900]),
            '30min': len([x for x in self._timestamps if now - x < 1800]),
            '60min': len([x for x in self._timestamps if now - x < 3600]),
            'created': self._created
        }


class AsyncStats(object):
    def __init__(self):
        self._pub_stats = {}

    def pub(self, topic):
        if topic not in self._pub_stats:
            self._pub_stats[topic] = PubStat(topic)
        self._pub_stats[topic].pub()

    @property
    def stats(self):
        return {k: v.stats for k, v in self._pub_stats.items()}