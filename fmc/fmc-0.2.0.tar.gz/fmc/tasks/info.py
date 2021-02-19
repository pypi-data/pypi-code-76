#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys, os
import logging

class InfoTask():

    def __init__(self, config_manager):
        self.config_manager = config_manager

    def print_env_info(self):
        logging.info(
"""
==============  configuration info =============
sys.path = %s

==============  configuration info =============
%s
==============  configuration end  =============
""" % (sys.path, self.config_manager.get_config_info()))
