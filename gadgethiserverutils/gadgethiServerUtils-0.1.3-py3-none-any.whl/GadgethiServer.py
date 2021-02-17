#-*-coding:utf-8 -*-
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import urllib.parse
from io import BytesIO, BufferedReader
import threading

from gadgethiServerUtils.exceptions import *
from gadgethiServerUtils.db_operations import *
from gadgethiServerUtils.file_basics import *

import datetime
import os
import json
import sys
import doctest
import yaml
import boto3
import logging

from urllib.parse import unquote
from pathlib import Path

from os.path import expanduser

class GadgetHiHTTPHandler(SimpleHTTPRequestHandler):
	"""
	This is the base handler of gadgethi http server. 
	"""
	server_configs = {}
	service_redirect = None

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@classmethod
	def initialize_configs(cls, configs):
		"""
		This is the function to initialize configs
		"""
		cls.server_configs.update(configs)

	@classmethod
	def initialize_service_redirect(cls, service_redirect):
		"""
		This is the function to initialize configs 
		"""
		cls.service_redirect = service_redirect

	def do_GET(self):
		print ("Inside server do_GET")
		d = {}
		d["method"] = "GET"
		d["values"] = {}
		self.send_response(200)
		self.end_headers()

		logging.info("IP address: "+self.client_address[0])

		wildcard_ip = False
		for allowed_ip in self.server_configs["allowed_ip"]:
			if '*' in allowed_ip:
				truncated_ip = allowed_ip[:allowed_ip.index('*')]
				logging.info("truncated_ip: "+truncated_ip)
				if truncated_ip in self.client_address[0]:
					wildcard_ip = True

		if self.client_address[0] not in self.server_configs["allowed_ip"] and not wildcard_ip:
			return {"indicator": False, "message": "IP not allowed"}

		try:
			self.split_query_string(self.path, d)
			response = self.service_redirect(d, **self.server_configs)

		except GadosServerError as e:
			print("GadosServerError = ",e)
			response = e.json_response

		except LackOfArgumentsError as e:
			print ("LackOfArgumentsError = ",e)
			response = e.json_response

		except Exception as e:
			_, _, exc_tb = sys.exc_info()
			fobj = traceback.extract_tb(exc_tb)[-1]
			fname = fobj.filename
			line_no = fobj.lineno

			gse = GadosServerError.buildfromexc(str(e), fname, line_no, ''.join(traceback.format_tb(exc_tb)))
			print("GadosServerError = ",gse)
			response = gse.json_response

		if type(response) is BufferedReader:
			# If it's the bufferedreader, meaning that it's an image,
			# read the response out and write it the thre registerfile
			self.wfile.write(response.read())
			response.close()
		elif type(response) is dict:
			# If it's a string, turn it into utf-8 encodings
			try:
				response_string_json = str(json.dumps(response))
			except:
				raise GadosServerError("Response not of type Json")

			self.wfile.write(bytes(response_string_json, 'utf-8'))
		else:
			self.wfile.write(bytes(str(response), 'utf-8'))

	def do_POST(self):
		print ("Inside server do_POST")
		d = {}
		d["method"] = "POST"
		d["values"] = {}
		d["form"] = {}

		content_length = int(self.headers['Content-Length'])
		content_type = self.headers['Content-Type']
		body = self.rfile.read(content_length)
		self.send_response(200)
		self.end_headers()

		logging.info("IP address: "+self.client_address[0])
		
		wildcard_ip = False
		for allowed_ip in self.server_configs["allowed_ip"]:
			if '*' in allowed_ip:
				truncated_ip = allowed_ip[:allowed_ip.index('*')]
				logging.info("truncated_ip: "+truncated_ip)
				if truncated_ip in self.client_address[0]:
					wildcard_ip = True

		if self.client_address[0] not in self.server_configs["allowed_ip"] and not wildcard_ip:
			return {"indicator": False, "message": "IP not allowed"}

		# Need a better way to figure out if an request is 
		# an image or not.
		handle_flag = True
		if content_type:
			logging.info("POST content_type: "+content_type)
			logging.info("[json body before decode]: "+str(body))
			if "application/x-www-form-urlencoded" in content_type:
				try:
					body = body.decode("utf-8")
					body = urllib.parse.unquote(body)

					# Try to decode it to utf-8 (if it's a string)
					self.split_body(body, d["form"])
				except:
					# If it's an image, don't need to decode
					self.split_body(body, d["form"])

			elif "application/json" in content_type:
				body = body.decode("utf-8")
				d["form"] = json.loads(body)

			else:
				handle_flag = False 

		# This needs to be fixed in the future
		if self.client_address[0] == "192.168.8.174":
			try:
				body = body.decode("utf-8")
				body = urllib.parse.unquote(body)

				# Try to decode it to utf-8 (if it's a string)
				self.split_body(body, d["form"])
			except:
				# If it's an image, don't need to decode
				self.split_body(body, d["form"])

		logging.info("POST body: "+str(d["form"]))

		if handle_flag:
			try:
				response = self.service_redirect(d, **self.server_configs)
			except GadosServerError as e:
				print("GadosServerError = ",e)
				response = e.json_response

			except LackOfArgumentsError as e:
				print("LackOfArgumentsError = ",e)
				response = e.json_response

			except Exception as e:
				_, _, exc_tb = sys.exc_info()
				fobj = traceback.extract_tb(exc_tb)[-1]
				fname = fobj.filename
				line_no = fobj.lineno

				gse = GadosServerError.buildfromexc(str(e), fname, line_no, ''.join(traceback.format_tb(exc_tb)))
				print("GadosServerError = ",gse)
				response = gse.json_response
				
			try:
				response_string_json = str(json.dumps(response))
			except:
				response_string_json = str(response)
		else:
			response_string_json = str(json.dumps({"indicator": False, "message": "Not supported content-type"}))

		self.wfile.write(bytes(response_string_json, 'utf-8'))

	def end_headers(self):
		# Can add CORS restrictions here
		SimpleHTTPRequestHandler.end_headers(self)

	# Helper Functions
	# -------------------------
	def split_body(self, body, dictionary):
		"""
		transform the http post to python dictionary

		>>> d = {}
		>>> d["form"] = {}
		>>> body = "way=1&lon=19.32940&len=2349"
		>>> split_body(body, d["form"])
		>>> print(d)
		{'form': {'way': '1', 'lon': '19.32940', 'len': '2349'}}
		"""
		try:
			out = body.split('&')
			for i in range(len(out)):
				out[i] = out[i].replace("+", " ")
		except:
			out = []

		for item in out:
			try:
				temp_list = item.split('=')
				dictionary[temp_list[0]] = temp_list[1]
			except:
				raise GadosServerError("decode get/post request error. item: "+item+" doesn't use the query format")

	def split_query_string(self, path, dictionary):
		"""
		transform the http query string to python dictionary

		>>> d = {}
		>>> d["values"] = {}
		>>> query = "/?way=1&lon=19.32940&len=2349"
		>>> split_query_string(query, d)
		>>> print(d)
		{'values': {'way': '1', 'lon': '19.32940', 'len': '2349'}}
		"""
		try:
			beginning = path.index('?')
			new_str = path[beginning+1:]
			new_str = urllib.parse.unquote(new_str)
		except:
			raise GadosServerError("decode get/post request error. Can't split the query string.")

		self.split_body(new_str, dictionary["values"])


class GadgetHiServer(HTTPServer):
	"""
	This is the main server. 
	"""
	def __init__(self, test=False, table_list=[], initialize_func_list=[], desc="GadgetHi Main", 
		yaml_exccondition=lambda :False, configs={}, service_handler=lambda: None, 
		http_handler_cls=None, config_path="", custom_event_handler=None):

		self.server_config = load_config(config_path)
		self.credentials_config = load_config(expanduser("~") + "/.gserver/credentials.yaml")
		self.server_api_path = self.server_config["server_api_path"]
		self.server_api_dict = read_config_yaml(self.server_api_path)

		init_log(self.server_config["log_file_path"])

		self.service_handler = service_handler
		self.http_handler = http_handler_cls
		self.desc = desc

		if not test:
			self.host = self.server_config["server_address"]
			self.port = int(self.server_config["server_port"])
		else:
			self.host = self.server_config["test_server_address"]
			self.port = int(self.server_config["test_server_port"])

		local_server_address = (self.host, self.port)
		super().__init__(local_server_address, self.http_handler)

		yaml_config = {}
		yaml_config.update(configs)
		yaml_config.update(self.server_config)
		yaml_config.update(self.credentials_config)

		# Initialization
		self.fetch_yamls(yaml_config, yaml_exccondition)
		GadgetHiHTTPHandler.initialize_configs(yaml_config)
		
		if custom_event_handler:
			GadgetHiHTTPHandler.initialize_service_redirect(custom_event_handler)
		else:
			GadgetHiHTTPHandler.initialize_service_redirect(self.redirectToServices)

		# db operations init
		generate_db_header(table_list)
		init_db_location(self.server_config)

		# db_operation, connect to correct database specified
		connect_to_database()

		for init_func in initialize_func_list:
			# This initialized all the tables
			init_func()

		print("*** Server Initialized ***")

	def run(self):
		"""
		execution function
		"""
		print('Starting %s Server at ' % self.desc, self.host, ' port: ', self.port)
		self.serve_forever()


	# Fetch yaml function
	# -----------------------
	def fetch_yamls(self, yaml_config, exceptcond=lambda :False):
		"""
		This is the helper function to fetch yamls from s3
		"""
		ACCESS_ID = yaml_config["aws_access_key_id"] 
		SECRET_KEY = yaml_config["aws_secret_access_key"] 
		
		# bucket and document location info
		bucket_name = yaml_config["yaml_s3_bucket"]
		s3_folder_header = yaml_config["yaml_s3_folder"] #"doday_yamls/"
		local_folder_header = yaml_config["yaml_local_folder"] #"sample_menu/"

		# database ini
		database_ini_path = yaml_config["s3_database_ini_path"] #"database_ini/database.ini"
		database_ini_local_path = yaml_config["local_database_ini_path"] #"util/database.ini"

		s3 = boto3.client('s3', aws_access_key_id=ACCESS_ID, aws_secret_access_key=SECRET_KEY)
		objects = s3.list_objects(Bucket=bucket_name, Prefix=s3_folder_header)["Contents"]
		print("Pulling Yamls....")
		for obj in objects:
			obj_name = obj["Key"].replace(s3_folder_header, "")
			if exceptcond(obj_name=obj_name):
				continue
			print(obj_name)
			s3.download_file(bucket_name, s3_folder_header+obj_name, local_folder_header+obj_name)

		# Also fetch database ini here -> no need to put the path to config here -> database ini should also be in util/
		s3.download_file(bucket_name, database_ini_path, database_ini_local_path)

	def redirectToServices(self, request_dict, **server_config):
		"""
		This helps redirect to various services
		in the management server.
		"""
		if ("form" in request_dict):
			srv = request_dict["form"]["service"]
		else:
			srv = request_dict["values"]["service"]

		try:
			if ("form" in request_dict):
				srv = request_dict["form"]["service"]
			else:
				srv = request_dict["values"]["service"]
		except:
			raise LackOfArgumentsError(["service"])
		try:
			method = request_dict['method']
		except:
			raise LackOfArgumentsError(['method'])

		try:
			api_context = self.server_api_dict["services"][srv]
		except:
			raise GadosServerError("Service Type not supported.")

		return self.service_handler(request_dict, api_context, method, **server_config)



