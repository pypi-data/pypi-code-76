#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from r3sponse.classes.config import *
from r3sponse.classes import utils
from r3sponse.classes.utils import color, symbol
from django.http import JsonResponse
import json as pypi_json

# the manager class.
class R3sponse(object):
	def __init__(self):	

		# set log file.
		self.log_file = None

		# set log level.
		self.log_level = 0
		#if utils.argument_present('--log-level'):
		#	try: self.log_level = int(utils.get_argument('--log-level'))
		#	except: self.log_level = 0
		#

	# response functions.
	def default_response(self):
		return self.ResponseObject()
	def success_response(self,
		# the message (must be param #1).
		message, 
		# additional returnable functions (must be param #2).
		variables={}, 
		# log log level of the message (int).
		log_level=None, 
		# save the error to the logs file.
		save=False,
		# return as a django JsonResponse.
		django=False,
	):
		response = self.default_response()
		response["success"] = True
		response["message"] = message
		response["error"] = None
		for key, value in variables.items():
			response[key] = value
		r3sponse.log(message=response["message"], log_level=log_level, save=save)
		if django: 
			try:
				response = JsonResponse(response.dict(), safe=False)
			except AttributeError:
				response = JsonResponse(response)
		return response
	def error_response(self,
		# the error message.
		error="", 
		# log log level of the message (int).
		log_level=None, 
		# save the error to the erros file.
		save=False,
		# return as a django JsonResponse.
		django=False,
	):
		response = self.default_response()
		response["success"] = False
		response["message"] = None
		response["error"] = error
		r3sponse.log(error=response["error"], log_level=log_level, save=save)
		if django: 
			try:
				response = JsonResponse(response.dict(), safe=False)
			except AttributeError:
				response = JsonResponse(response)
		return response
		#
	def success(self, response):
		if response["error"] == None:
			return True
		else: return False

	# parameter functions.
	def get_request_parameter(self, request, identifier):
		response = self.default_response()
		format = None
		if ":" in identifier:
			identifier,format = identifier.split(":")
			while True:
				if " " in format: format = format.replace(" ","")
				else: break
		if request.method in ["post", "POST"]:
			variable = request.POST.get(identifier)
		else:
			variable = request.GET.get(identifier)
		if variable in ["", None]:
			return variable, self.error_response(f"Define parameter: [{identifier}].")
		elif format != None:
			if format in ["str", "string"]: variable = str(variable)
			elif format in ["int", "integer"]: variable = int(variable)
			elif format in ["bool", "boolean"]: 
				if variable in ["true", "True", "TRUE", True]: variable = True
				else: variable = False
			elif format in ["float", "double"]: variable = float(variable)
			elif format in ["array", "list"]: variable = variable.split(",")
			else:
				raise ValueError(f"Unrecognized <r3sponse.get_request_parameter> format: {format}.")
		return variable, self.success_response(f"Succesfully retrieved request parameter [{identifier}].", {
			"key":identifier,
			"value":variable,
		})
	def get_request_parameters(self, request, identifiers=[], optional=False, empty_value=None):
		if isinstance(identifiers, str):
			return self.error_response("__get_request_params__ is used to retrieve several identifiers (array format not string).")
		params = self.ResponseObject()
		for param in identifiers:
			param_value, response = self.get_request_parameter(request, param)
			param = param.split(":")[0]
			if response["error"] != None: 
				if optional:
					params[param] = empty_value
				else:
					return params, response
			else: 
				params[param] = param_value
		if optional:
			for key in identifiers:
				try: params[key]
				except: params[key] = empty_value
		return params, self.success_response(f"Succesfully retrieved {len(params)} request parameter(s).")

	# check parameters.
	def check_parameter(self, parameter=None, name="parameter", empty_value=None):
		response = self.default_response()
		if parameter == empty_value: 
			return self.error_response(f"Define parameter [{name}].")
		if ":" in name:
			name,formats = name.split(":")
			while True:
				if " " in formats: formats = formats.replace(" ","")
				else: break
			formats = formats.split(",")
			param_format = Formats.get(parameter, serialize=True)
			if param_format not in formats:
				return self.error_response(f"Incorrect parameter [{name}:{param_format}] format, correct format(s): {Files.Array(path=False, array=formats).string(joiner=', ')}.")
		return self.success_response(f"Succesfully checked parameter [{name}].")
	def check_parameters(self, parameters={"parameter":None}, empty_value=None):
		response = self.default_response()
		for id, value in parameters.items():
			response = self.check_parameter(value, id, empty_value=empty_value)
			if response["error"] != None: return response
		return response

	# log functions.
	def log(self, 
		# option 1:
		# the message.
		message=None,
		# option 2:
		# the error.
		error=None,
		# option 3:
		# the response dict (leave message None to use).
		response={},
		# print the response as json.
		json=False,
		# optionals:
		# the log level for printing to console.
		log_level=0,
		# save to log file.
		save=False,
		# save errors only (for option 2 only).
		save_errors=False,
	):
		msg, _error_ = None, False
		if [message,error,response] == [None,None,{}]:
			raise ValueError("Define either parameter [message:str], [error:str] or [response:dict].")
		if response != {}:
			if response["error"] != None: 
				_error_ = True
				msg = f"Error: {response['error']}"
			else: 
				msg = response["message"]
		elif error != None: 
			msg = f"Error: {error}"
		else: 
			msg = message
		try:
			comparison = log_level != None and log_level >= self.log_level
		except TypeError as e:
			if "not supported between instances of 'dict' and 'int'" in f"{e}":
				raise TypeError(f"You most likely returned a r3sponse.error_response when you meant a r3sponse.success_response, error: {e}")
			else:
				raise TypeError(e)
		if comparison:
			#print(f"{Formats.Date().seconds_timestamp} - {color.fill(msg)}")
			if json:
				if response != {}:
					print(response.json())
				elif error != None:
					print(self.error_response(error))
				else:
					print(self.success_response(message))
			else:
				print(f"{color.fill(msg)}")
		if save: 
			self.__log_to_file__(msg)
		elif save_errors and _error_:
			self.__log_to_file__(msg)

		#
	def load_logs(self, format="webserver", options=["webserver", "cli", "array", "string"]):
		try:
			logs = Formats.File(self.log_file, load=True, blank="").data
		except:
			return self.error_response("Failed to load the logs.")
		if format == "webserver":
			logs = logs.replace("\n", "<br>")
		elif format == "cli":
			a=1
		elif format == "array" or format == list:
			logs = logs.split("\n")
		elif format == "string" or format == str:
			logs = str(logs)
		else: 
			return self.error_response(f"Invalid format parameter [{format}], valid options: {options}.")

		return self.success_response("Succesfully loaded the logs.", {"logs":logs})
	def reset_logs(self):
		Formats.File(self.log_file).save(f"Resetted log file.\n")
		#
	
	# system functions.
	def __log_to_file__(self, message):

		# init.
		response = self.default_response()
		try:
			with open(self.log_file, "a") as file:
				file.write(f'{Formats.Date().seconds_timestamp} - {message}\n')
			response["success"] = True
			response["message"] = "Succesfully logged the message."
		except:
			response["error"] = "Failed to log the message."
			return response
		
		# check file size.
		size = Formats.FilePath(self.log_file).size(mode="mb", type="integer")
		if int(size.replace(" MB", "")) >= 100: self.reset_logs()

		# return response.
		return response

		#

	# a response object.
	def serialize(self, response={}):
		if isinstance(response, str):
			try:
				response = ast.literal_eval(response)
			except:
				response = json.loads(response)
		for key in list(response.keys()):
			value = response[key]
			no_dict = False
			if isinstance(value, dict):
				value = self.serialize(value)
			else:
				try:
					value = ast.literal_eval(value)
				except:
					try:
						value = json.loads(value)
					except:
						no_dict = True
				if no_dict == False and isinstance(value, dict):
					value = self.serialize(value)
			if no_dict == False: a=1
			elif value in [True, "True", "true", "TRUE"]: value = True
			elif value in [False, "False", "false", "FALSE"]: value = False
			elif isinstance(value, str):
				if "." in value:
					try: value = float(value)
					except: a=1
				else:
					try: value = int(value)
					except: a=1
			response[key] = value
		return response
	def response(self, response={
			"success":False,
			"message":None,
			"error":None,
	}):
		return self.ResponseObject(response)
	def safe_response(self, response={
			"success":False,
			"message":None,
			"error":None,
	}):
		return self.response(self.serialize(response))
	class ResponseObject(object):
		def __init__(self, 
			# the response attributes.
			attributes={
				"success":False,
				"message":None,
				"error":None,
			},
			# import a dumped json response (str) (ignores attributes).
			json=None,
		):
			if isinstance(json, str):
				self.assign(pypi_json.loads(Formats.String(json).slice_dict()))
			elif isinstance(json, dict):
				self.assign(json)
			elif json != None:
				raise ValueError("Invalid usage, the r3sponse.ResponseObject json parameter must be str / dict format.")
			else:
				self.assign(attributes)

			# check error passed as success response.
			if isinstance(self.message, str) and self.message.split(" ")[0] == "Failed":
				#_traceback_.print_exc() 
				raise ValueError("The first word of a success response may not be [Failed].")
		# iterate over self keys & variables.
		def items(self):
			return vars(self).items()
		def keys(self):
			return list(vars(self).keys())
		def values(self):
			return list(vars(self).values())
		def dict(self, serializable=False, json=False):
			dictionary = {}
			for key, value in self.items():
				if serializable:
					if isinstance(value, object) and not isinstance(value, dict) and not isinstance(value, list):
						value = str(value)
					elif isinstance(value, str) or isinstance(value, bool) or value == None:
						if value in [True, "True", "True".lower()]: 
							if json:
								value = "true"
							else: 
								value = True
						elif value in [False, "False", "False".lower()]: 
							if json:
								value = "false"
							else: 
								value = False
						elif value in [None, "None", "None".lower()]: 
							if json:
								value = "null"
							else: 
								value = None
				dictionary[key] = value
			return dictionary
		# assign self variables by dictionary.
		def assign(self, dictionary):
			if not isinstance(dictionary, dict):
				raise TypeError("You can only self assign with a dictionary as parameter.")
			for key,value in dictionary.items():
				if value in ["False", "false"]: value = False
				elif value in ["True", "true"]: value = True
				elif value in ["None", "none", "null", "nan"]: value = None
				else:
					if isinstance(value, str):
						if "." in str(value):
							try: value = float(value)
							except: a=1
						else:
							try: value = int(value)
							except: a=1
				self[key] = value
		# unpack keys as tuple.
		def unpack(self, 
			# the variable keys (#1 parameter).
			keys=[],
		):
			list = []
			for key in keys:
				list.append(self[key])
			return list
		# clean default values.
		def clean(self):
			for i in ["error", "message", "success"]:
				del self[i]
				#except: a=1
			return self
		# crash the error message.
		def crash(self, error="ValueError", traceback=True, json=False):
			if json:
				r3sponse.log(error=self["error"], json=json)
				sys.exit(1)
			else:
				if not traceback:
					sys.tracebacklimit = -1 ; sys.traceback_limit = -1
				if error.lower() in ["valueerror"]: raise Exception(self["error"])
				else: raise Exception(self["error"])
		# count items.
		def __len__(self):
			return len(self.keys())
		# support item assignment.
		def __setitem__(self, key, value):
			setattr(self, key, value)
		def __getitem__(self, key):
			return getattr(self, key)
		def __delitem__(self, key):
			delattr(self, key)
		# string format.
		def __str__(self):
			return self.json(indent=4) 
		def json(self, indent=4):
			return json.dumps(self.dict(serializable=True, json=True), indent=indent).replace(': "None"', ': null').replace(': "False"', ': false').replace(': "True"', ': true')
		#def __dict__(self):
		#	return json.dumps(self.dict(), indent=4)

# initialized objects.
r3sponse = R3sponse()

