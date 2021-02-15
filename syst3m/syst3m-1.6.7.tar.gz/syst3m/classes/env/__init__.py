#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from syst3m.classes.config import *

# the env object class.
class Env(object):
	def __init__(self):
		a=1
		#
	def fill(self, string):
		c = 0
		for i in range(string.count("$")):
			c += 1
			if string[0] == "$" and c == 1:
				variable_id, _ = Formats.String(string.split("$")[1]).before_after_first_occurence(slicer=["/","+",">","<","?",";",":","|","\\","]","[","{","}","=","+","(",")","!","@","#","$","%","^","&","*","±","~","`","'",'"'," "], include_after=True)
			else:
				variable_id, _ = Formats.String(string.split("$")[c]).before_after_first_occurence(slicer=["/","+",">","<","?",";",":","|","\\","]","[","{","}","=","+","(",")","!","@","#","$","%","^","&","*","±","~","`","'",'"'," "], include_after=True)
			for i in ["/","+",">","<","?",";",":","|","\\","]","[","{","}","=","+","(",")","!","@","#","$","%","^","&","*","±","~","`","'",'"'," "]:
				variable_id = variable_id.replace(i, "")
			variable = os.environ.get(variable_id)
			if variable == None: raise ValueError(f"Required environment variable {variable_id} is undefined.")
			variable = self.get_string(variable)
			string = string.replace(f"${variable_id}", variable)
		string = string.replace("~",HOME)
		return string
	# get.
	def get(self, id, default=None, format="str"):
		if format in [str, "str", "string"]:
			return self.get_string(id, default=default)
		elif format in [bool, "bool", "boolean"]:
			return self.get_boolean(id, default=default)
		elif format in [int, float, "int", "float", "integer", "double"]:
			return self.get_integer(id, default=default)
		elif list in [list, "list", "array"]:
			return self.get_array(id, default=default)
		elif dict in [dict, "dict", "dictionary", "json"]:
			return self.get_dictionary(id, default=default)
		else: raise ValueError(f"Unkown format: {format}.")
	def get_string(self, id, default=None):
		e = os.environ.get(id)
		if e == None: 
			return default
		else:
			return e
	def get_boolean(self, id, default=None):
		e = os.environ.get(id)
		if e == None: 
			return default
		elif e in [True, "True", "true", "TRUE"]:
			return True
		else: 
			return False
	def get_integer(self, id, default=None):
		e = os.environ.get(id)
		try:
			if "." in str(e):
				return float(e)
			else:
				return int(e)
		except:
			return default
	def get_array(self, id, default=None):
		e = os.environ.get(id)
		if e == None: 
			return default
		else: 
			a = []
			for i in e.split(","):
				a.append(self.__remove_whitespace__(i))
			return a
	def get_tuple(self, id, default=None):
		e = os.environ.get(id)
		if e == None: 
			return default
		else: 
			a = []
			for i in e.split(","):
				a.append(self.__remove_whitespace__(i))
			return tuple(a)
	def get_dictionary(self, id, default=None):
		e = os.environ.get(id)
		if e == None: 
			return default
		else: 
			a = []
			for i in e.split(","):
				a.append(self.__remove_whitespace__(i))
			d = {}
			for i in a:
				try:
					key,value = i.split(":")
					d[self.__remove_whitespace__(key)] = self.__remove_whitespace__(value)
				except: a=1
			return tuple(a)
	# set.
	def set(self, id, value, format="unknown"):
		if format == "unknown": format = Formats.get(value, serialize=True)
		if format in [str, "str", "string"]:
			self.set_string(id, value)
		elif format in [bool, "bool", "boolean"]:
			self.set_boolean(id, value)
		elif format in [int, float, "int", "float", "integer", "double"]:
			self.set_integer(id, value)
		elif list in [list, "list", "array"]:
			self.set_array(id, value)
		elif dict in [dict, "dict", "dictionary", "json"]:
			self.set_dictionary(id, value)
		else: raise ValueError(f"Unkown format: {format}.")
	def set_string(self, id, value):
		os.environ[id] = value
	def set_boolean(self, id, value):
		if e in [True, "True", "true", "TRUE"]:
			os.environ[id] = "true"
		else: 
			os.environ[id] = "false"
	def set_integer(self, id, value):
		os.environ[id] = str(value)
	def set_array(self, id, value):
		os.environ[id] = Formats.Array(value).string(joiner=",")
	def set_tuple(self, id, value):
		os.environ[id] = Formats.Array(value).string(joiner=",")
	def set_dictionary(self, id, value, subkey=""):
		for key, value in value.items():
			if subkey == "": lkey = key
			else: lkey = f"{subkey}_{key}"
			if isinstance(value, dict):
				self.set_dictionary(key, value, subkey=lkey)
			else: 
				self.set(lkey, value, format="unknown")
	# system functions.
	def __remove_whitespace__(self, string):
		if isinstance(string, str):
			for attempts in range(101):
				if string[0] == " ":
					string = string[1:]
				elif string[len(string)-1] == " ":
					string = string[:-1]
				else: break
		return string
	

# initialized classes.
env = Env()