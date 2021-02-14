#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from syst3m.classes.config import *
from syst3m.classes import objects

# the default cache object class.
class Default(objects.Object):
	def __init__(self, path=None):
		if path == None: path = f"{HOME}/.cache/"
		if not os.path.exists(path): os.mkdir(path)
		objects.Object.__init__(self)
		self.assign({
			"path":path,
		})
	def set(self, data=None, group=None, id=None, format="str"):
		if id == None:
			data_path = f"{self.path}/{group}"
		else:
			data_path = f"{self.path}/{group}/"+id.replace("/", "\\")
			base = Formats.FilePath(data_path).base()
			if not os.path.exists(base): os.system(f"mkdir {data_path}")
		if format in [str, "str", "string", int, float, "int", "integer", "float", "double"]:
			Files.save(data_path, str(data), format="str")
		elif format in [dict, list, "dict", "dictionary", "list", "array", "json"]:
			Files.save(data_path, str(data), format="json")
		else:
			raise ValueError(f"Unkown format: {format}.")
	def get(self, group=None, id=None, format="str"):
		if id == None:
			data_path = f"{self.path}/{group}"
		else:
			data_path = f"{self.path}/{group}/"+id.replace("/", "\\")
			base = Formats.FilePath(data_path).base()
			if not os.path.exists(base): os.system(f"mkdir {data_path}")
		def load():
			if format in [str, "str", "string"]:
				return Files.load(data_path, format="str")
			elif format in [int, "int", "integer"]:
				return int(Files.load(data_path, format="str"))
			elif format in [float, "float", "double"]:
				return float(Files.load(data_path, format="str"))
			elif format in [dict, list, "dict", "dictionary", "list", "array", "json"]:
				return Files.load(data_path, format="json")
			else:
				raise ValueError(f"Unkown format: {format}.")
		try:
			loaded = load()
		except FileNotFoundError:
			self.set(id=id, data="None", group=group, format=format)
			loaded = load()
		if loaded in ["None","none","null"]: loaded = None
		return loaded


# the default cache.
cache = Default()

# the webserver cache object class.
class WebServer(syst3m.objects.Thread):
	def __init__(self,
		id="webserver",
		host="127.0.0.1",
		port=52379,
		path=None,
		default={},
	):
		syst3m.objects.Thread.__init__(self)
		self.__cache__ = Default(path=path)
		self.assign({
			"sleeptime":3,
			"id":id,
			"host":host,
			"port":port,
			"cache":default,
		})
	def set(self, group=None, id=None, value=None):
		response = requests.get(f'http://{self.host}:{self.port}/set?{urllib.parse.urlencode({
			"key":key,
			"id":id,
			"value":value,
			"token":self.token(),
		})}')
		try:
			response = response.json()
		except:
			return r3sponse.error_response(f"Failed to serialize output: {response}, status code {response.status_code}")
		return r3sponse.ResponseObject(response)
	def get(self, group=None, id=None):
		response = requests.get(f'http://{self.host}:{self.port}/get?{urllib.parse.urlencode({
			"key":key,
			"token":self.token(),
		})}')
		try:
			response = response.json()
		except:
			return r3sponse.error_response(f"Failed to serialize output: {response}, status code {response.status_code}")
		return r3sponse.ResponseObject(response)
	def app(self):
		app = flask.Flask(__name__)
		@app.route('/get')
		def get():
			token = request.args.get('token')
			if token != self.token():
				return r3sponse.error_response(f"Provided an invalid token {token}.").json()
			key = request.args.get('key')
			id = request.args.get('id')
			if id in ["none", "null", "None"]: id = None
			try:
				if id == None:
					value = self.cache[key]
				else:
					value = self.cache[key][id]
			except KeyError:
				return r3sponse.error_response(f"There is no value cached for key {key}.").json()
			return r3sponse.success_response(f"Successfully retrieved {key}.", {
				"key":key,
				"value":value,
			}).json()
		@app.route('/set')
		def set__(self):
			token = request.args.get('token')
			if token != self.token():
				return r3sponse.error_response(f"Provided an invalid token {token}.").json()
			key = request.args.get('key')
			id = request.args.get('id')
			if id in ["none", "null", "None"]: id = None
			value = request.args.get('value')
			if id == None:
				self.cache[key] = value
			else:
				try: self.cache[key]
				except KeyError: self.cache[key] = {}
				self.cache[key][id] = value
			return r3sponse.success_response(f"Successfully cached {key}.").json()
		@app.route('/active')
		def active__(self):
			token = request.args.get('token')
			if token != self.token():
				return r3sponse.error_response(f"Provided an invalid token {token}.").json()
			return r3sponse.success_response(f"Active.").json()
		app.run(host=self.host, port=self.port)
	def token(self):
		if random.randrange(1, 100) <= 5: 
			self.__cache__.set(group=self.id, id="token", data=Formats.String("").generate(length=64, digits=True, capitalize=True))
		return self.__cache__.get(group=self.id, id="token")
	def running(self):
		response = requests.get(f'http://{self.host}:{self.port}/active?{urllib.parse.urlencode({
			"key":key,
			"token":self.token(),
		})}')
		#try:
		response = response.json()
		#except:
		#	return False
		return True
	def run(self):
		self.__cache__.set(group=self.id, id="daemon", data="*running*")
		self.__cache__.set(group=self.id, id="token", data=Formats.String("").generate(length=64, digits=True, capitalize=True))
		self.app()
		self.__cache__.set(group=self.id, id="daemon", data="*stopped*")
