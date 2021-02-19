#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" A simple python script

"""
__author__ = 'Otger Ballester'
__copyright__ = 'Copyright 2020'
__date__ = '25/06/2020'
__credits__ = ['Otger Ballester', ]
__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Otger Ballester'
__email__ = 'otger@ifae.es'

import json


class AsyncStats(object):
    txt_list = ['bad_msg', 'cb_exc', 'cb_calls', 'cb_reg']

    def __init__(self):
        self._topics = {}
        self._unknown_topics = {}
        self._nonAsyncMSG_recv = 0

    def new_topic(self, topic):
        topic = str(topic)
        if topic not in self._topics:
            self._topics[topic] = {k: 0 for k in self.txt_list}

    def bad_msg(self, topic=None):
        """ Received a MSG from a topic which could not be recreated from its json bytes"""
        if topic is None:
            self._nonAsyncMSG_recv += 1
            return
        topic = str(topic)
        self._topics[topic]['bad_msg'] += 1

    def exception(self, topic):
        """Exception on callback"""
        topic = str(topic)
        self._topics[topic]['cb_exc'] += 1

    def cb_call(self, topic):
        """Calling callbacks on topic"""
        topic = str(topic)
        self._topics[topic]['cb_calls'] += 1

    def cb_reg(self, topic):
        """A new callback has been registered"""
        topic = str(topic)
        self._topics[topic]['cb_reg'] += 1

    def unknown_topic(self, topic):
        """A message for an unknown topic has been received"""
        topic = str(topic)
        if topic not in self._unknown_topics:
            self._unknown_topics[topic] = 0
        self._unknown_topics[topic] += 1

    def as_json(self):
        return json.dumps({'registered': self._topics, 'unknown': self._unknown_topics})

