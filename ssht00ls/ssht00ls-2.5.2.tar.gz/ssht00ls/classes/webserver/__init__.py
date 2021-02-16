#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os
os.environ["SSHT00LS_WEBSERVER_IMPORT"] = "True"
from ssht00ls.classes.config import *

# the ssync object class.
class WebServer(syst3m.cache.WebServer):
	def __init__(self):
		syst3m.cache.WebServer.__init__(self, serialized={
			"id":"ssht00ls-agent",
			"path":f"{HOME}/.{ALIAS}/.cache/",
			"host":"127.0.0.1",
			"default":{},
			"port":52379,
		})
	def start_daemon(self, daemon, group="daemons", id=None):
		self.__cache__.set(group=group, id=id, data=daemon)
		daemon.start()
