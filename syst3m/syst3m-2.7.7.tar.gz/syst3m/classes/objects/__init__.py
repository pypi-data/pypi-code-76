#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from syst3m.classes.config import *

# object.
class Object(object):
	def __init__(self):
		a=1
	# iterate over self keys & variables.
	def items(self):
		return vars(self).items()
	def keys(self):
		return list(vars(self).keys())
	def values(self):
		return list(vars(self).values())
	def dict(self):
		dictionary = {}
		for key, value in self.items():
			dictionary[key] = value
		return dictionary
	# assign self variables by dictionary.
	def assign(self, dictionary):
		if not isinstance(dictionary, dict):
			raise TypeError("You can only self assign with a dictionary as parameter.")
		for key,value in dictionary.items():
			self[key] = value
	# support item assignment.
	def __setitem__(self, key, value):
		setattr(self, key, value)
	def __getitem__(self, key):
		return getattr(self, key)
	def __delitem__(self, key):
		delattr(self, key)

# thread.
class Thread(threading.Thread):
	def __init__(self, 
		# the threads id.
		id="Object",
		# the threads log level.
		log_level=0,
	):
		threading.Thread.__init__(self)
		self.log_level = log_level
		self.id = id
	# stop the thread.
	def run(self):
		r3sponse.log(f"Starting thread {self.id}.", log_level=self.log_level)
		self.running = True
		self.__run__()
		self.running = "stopped"
	def stop(self, timeout=120, sleeptime=1):
		self.running = False
		for i in range(timeout/sleeptime):
			if self.running == "stopped": break
			time.sleep(sleeptime)
		if self.running != "stopped": raise ValueError(f"Unable to stop thread {self}.")
		r3sponse.log(f"Stopped thread {self.id}.", log_level=self.log_level)
	def should_stop(self):
		return not self.running
	# iterate over self keys & variables.
	def items(self):
		return vars(self).items()
	def keys(self):
		return list(vars(self).keys())
	def values(self):
		return list(vars(self).values())
	def dict(self):
		dictionary = {}
		for key, value in self.items():
			dictionary[key] = value
		return dictionary
	# assign self variables by dictionary.
	def assign(self, dictionary):
		if not isinstance(dictionary, dict):
			raise TypeError("You can only self assign with a dictionary as parameter.")
		for key,value in dictionary.items():
			self[key] = value
	# support item assignment.
	def __setitem__(self, key, value):
		setattr(self, key, value)
	def __getitem__(self, key):
		return getattr(self, key)
	def __delitem__(self, key):
		delattr(self, key)
		