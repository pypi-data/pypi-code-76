#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import syst3m, encrypti0n
from fil3s import *
from r3sponse import r3sponse

# the encryption object class.
class Encryption(object):
	def __init__(self,
		# the configuration file (Dictionary).
		config=Dictionary,
		# the webserver cache (syst3m.cache.WebServer).
		webserver=syst3m.cache.WebServer, 
		# encrypted cache path.
		cache=None,
		# the passphrase (optional to prompt) (str).
		passphrase=None,
		# the interactive mode (prompt for password) (bool).
		interactive=True,
	):

		# init.
		self.config = config
		self.webserver = webserver
		self.passphrase = passphrase
		self.interactive = interactive
		self.cache = cache

		# vars.
		self._activated = False

		# checks.
		if webserver == None:
			return r3sponse.error("<ssht00ls.classes.encryption.generate>: Define parameter [webserver].", json=syst3m.defaults.options.json)
		elif not isinstance(webserver, syst3m.cache.WebServer):
			return r3sponse.error("<ssht00ls.classes.encryption.generate>: Parameter [webserver] requires to be instance syst3m.cache.WebServer.", json=syst3m.defaults.options.json)
		elif config == None:
			return r3sponse.error("<ssht00ls.classes.encryption.generate>: Define parameter [config].", json=syst3m.defaults.options.json)
		elif not isinstance(config, Dictionary):
			return r3sponse.error("<ssht00ls.classes.encryption.generate>: Parameter [config] requires to be instance Dictionary.", json=syst3m.defaults.options.json)

		# initialize.
		self.encryption = encrypti0n.aes.AsymmetricAES(
			public_key=self.config["encryption"]["public_key"],
			private_key=self.config["encryption"]["public_key"],
			passphrase=self.passphrase,
			memory=True,)
		self.database = encrypti0n.aes.Database(path=self.cache, aes=self.encryption)

	# generate encryption.
	def generate(self,
		# the passphrase (optional to prompt) (str).
		passphrase=None,
		# the verify passphrase (optional).
		verify_passphrase=None,
	):
		if passphrase != None: passphrase = self.passphrase
		if passphrase == None:
			if not self.interactive:
				return r3sponse.error("<ssht00ls.classes.encryption.generate>: Define parameter [passphrase].", json=syst3m.defaults.options.json)
			else:
				passphrase = getpass.getpass("Enter the passphrase of the ssht00ls encryption:")
		elif len(passphrase) < 8: 
			return r3sponse.error("The passphrase must contain at least 8 characters.", json=syst3m.defaults.options.json)
		elif passphrase.lower() == passphrase: 
			return r3sponse.error("The passphrase must contain capital characters.", json=syst3m.defaults.options.json)
		elif (self.interactive and passphrase != getpass.getpass("Enter the same passphrase:")) or (verify_passphrase != None and passphrase != verify_passphrase): 
			return r3sponse.error("The passphrase must contain at least 8 characters.", json=syst3m.defaults.options.json)
		self.encryption.rsa.passphrase = passphrase
		self.passphrase = passphrase
		response = self.encryption.generate_keys()
		if not response["success"]: 
			return r3sponse.error(f"Encoutered an error while generating the master encryption key: {response['error']}", json=syst3m.defaults.options.json)
		self.encryption.rsa.private_key = response.private_key
		self.encryption.rsa.public_key = response.public_key
		try: self.config["encryption"]
		except KeyError: self.config["encryption"] = {}
		self.config["encryption"]["public_key"] = self.encryption.rsa.public_key
		self.config["encryption"]["private_key"] = self.encryption.rsa.private_key
		self.config.save()
		response = self.encryption.load_keys()
		if not response["success"]: 
			return r3sponse.error(f"Encoutered an error while activating the ssht00ls encryption: {response['error']}", json=syst3m.defaults.options.json)
		response = self.webserver.set(group="passphrases", id="master", data=passphrase)
		if not response["success"]: 
			return r3sponse.error(f"Encoutered an error while caching the passphrase (#1): {response['error']}", json=syst3m.defaults.options.json)
		return r3sponse.success("Successfully generated the encryption.", json=syst3m.defaults.options.json)

	# activate encryption.
	def activate(self,
		# the key's passphrase (optional to retrieve from webserver) (str).
		passphrase=None, 
	):
		self._activated = False
		if passphrase != None: passphrase = self.passphrase
		if passphrase == None:
			response, new, passphrase = self.webserver.get(group="passphrases", id="master"), False, None
			if not response.success: return response
			elif response["success"]: passphrase = response["data"]
			if passphrase in [False, None, "", "null", "None", "none"]:
				if not self.interactive:
					return r3sponse.error("<ssht00ls.classes.encryption.activate>: Define parameter [passphrase].", json=syst3m.defaults.options.json)
				else:
					new = True
					passphrase = getpass.getpass("Enter the passphrase of the ssht00ls encryption:")
		self.encryption.rsa.passphrase = passphrase
		self.passphrase = passphrase
		response = self.encryption.load_keys()
		if not response["success"]: 
			return r3sponse.error(f"Encoutered an error while activating the ssht00ls encryption: {response['error']}", json=syst3m.defaults.options.json)
		response = self.database.activate()
		if not response["success"]: 
			return r3sponse.error(f"Encoutered an error while activating the encrypted cache: {response['error']}", json=syst3m.defaults.options.json)
		if new:
			response = self.webserver.set(group="passphrases", id="master", data=passphrase)
			if not response["success"]: 
				return r3sponse.error(f"Encoutered an error while caching the passphrase (#2): {response['error']}", json=syst3m.defaults.options.json)
		self._activated = True
		return r3sponse.success("Successfully activated the encryption.", json=syst3m.defaults.options.json)
	# properties.
	@property
	def activated(self):
		return self._activated
	@property
	def generated(self):
		return self.encryption.rsa.private_key != None and self.encryption.rsa.public_key != None
	
