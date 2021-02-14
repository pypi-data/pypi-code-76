#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from ssht00ls.classes.config import *
from ssht00ls.classes import utils

# the aliases object class.
class Aliases(object):
	def __init__(self):
		a=1
	def check(self, alias):
		try: CONFIG["aliases"][alias]
		except KeyError:
			return r3sponse.error_response(f"Alias {alias} does not exist.")
		return r3sponse.success_response(f"Successfully checked alias {alias}.")
	def delete(self, alias):
		response = self.check(alias)
		if not response["success"]: return response
		del CONFIG["aliases"][alias]
		CONFIG.save()
		return r3sponse.success_response(f"Successfully deleted alias {alias}.")
	def create(self, 
		# the alias.
		alias=None,
		# the users.
		username=None, 
		# the ip of the server.
		public_ip=None,
		private_ip=None,
		# the port of the server.
		public_port=None,
		private_port=None,
		# the path to the private key.
		key=None,
		# the keys passphrase.
		passhrase=None,
		# smart card.
		smart_card=False,
		# the smart cards pincode.
		pin=None,
		# save to configuration.
		save=True,
		# serialized all parameters as dict, except: [save].
		serialized={},
	):
		
		# serialized
		if serialized != {}:
			try:username = serialized["username"]
			except KeyError: username = None
			try:public_ip = serialized["public_ip"]
			except KeyError: public_ip = None
			try:private_ip = serialized["private_ip"]
			except KeyError: private_ip = None
			try:public_port = serialized["public_port"]
			except KeyError: public_port = None
			try:private_port = serialized["private_port"]
			except KeyError: private_port = None
			try:key = serialized["key"]
			except KeyError: key = None
			try:passphrase = serialized["passphrase"]
			except KeyError: passphrase = None
			try:smart_card = serialized["smart_card"]
			except KeyError: smart_card = None
			try:pin = serialized["pin"]
			except KeyError: pin = None
			try:alias = serialized["alias"]
			except KeyError: alias = None

		# checks.
		success, response = utils.__check_parameters__({
			"alias":alias,
			"username":username,
			"public_ip":public_ip,
			"private_ip":private_ip,
			"public_port":public_port,
			"private_port":private_port,
			"key":key,
		}, empty_value=None)
		if not success: return response
		if smart_card:
			success, response = utils.__check_parameters__({
				"pin":pin,
			}, empty_value=None)
			if not success: return response
		else:
			success, response = utils.__check_parameters__({
				"passphrase":passphrase,
			}, empty_value=None)
			if not success: return response
		key = syst3m.env.fill(key)
		json_config = {}
		if NETWORK_INFO["public_ip"] == public_ip:
			ip = private_ip
			port = private_port
		else:
			ip = public_ip
			port = public_port
		
		# create config.
		config += f"\nHost {alias}"
		json_config["public_ip"] = public_ip
		json_config["private_ip"] = private_ip
		config += "\n    HostName {}".format(ip)
		json_config["public_port"] = public_port
		json_config["private_port"] = private_port
		config += "\n    Port {}".format(port)
		json_config["user"] = username
		config += "\n    User {}".format(username)
		config += "\n    ForwardAgent yes"
		config += "\n    PubKeyAuthentication yes"
		#config += "\n    IdentitiesOnly yes"
		if not smart_card:
			json_config["key"] = key
			json_config["smart_card"] = False
			config += "\n    IdentityFile {}".format(key)
		else:
			json_config["key"] = smart_cards.path
			json_config["smart_card"] = True
			config += "\n    PKCS11Provider {}".format(smart_cards.path)

		# save.
		if save:
			CONFIG["aliases"][alias] = json_config
			if smart_card:
				response = ENCRYPTION.encrypt(str(pin))
				if not response["success"]: return response
				CONFIG["aliases"][alias]["pin"] = response["encrypted"].decode()
			else:
				response = ENCRYPTION.encrypt(str(passhrase))
				if not response["success"]: return response
				CONFIG["aliases"][alias]["passhrase"] = response["encrypted"].decode()
			CONFIG.save()

		# response.
		return r3sponse.success_response(f"Successfully created alias [{alias}].", {
			"json":json_config,
			"str":config,
		})
	def synch(self):
		if not os.path.exists(f"{HOME}/.ssh"): os.system(f"mkdir {HOME}/.ssh && chown -R {OWNER}:{GROUP} {HOME}/.ssh && chmod 700 {HOME}/.ssh")
		include = f"include ~/.ssht00ls/lib/aliases"
		if not os.path.exists(f"{HOME}/.ssh/config"): 
			Files.save(f"{HOME}/.ssh/config", include)
			os.system(f"chown {OWNER}:{GROUP} {HOME}/.ssh/config && chmod 770 {HOME}/.ssh/config")
		if include not in Files.load(f"{HOME}/.ssh/config"):
			Files.save(f"{HOME}/.ssh/config", Files.load(f"{HOME}/.ssh/config")+"\n"+include+"\n")
		aliases, c = "", 0
		for alias, info in CONFIG["aliases"].items():
			if "example.com " not in alias:
				checked = Files.Dictionary(path=False, dictionary=info).check(default={
					"alias":None,
					"username":None,
					"public_ip":None,
					"private_ip":None,
					"public_port":None,
					"private_port":None,
					"key":None,
					"passhrase":None,
					"smart_card":None,
					"pin":None,
				})
				response = self.create(save=False, serialized=checked)
				if not response["success"]: return response
				aliases += response["str"]
				c += 1
		Files.save(f"{HOME}/.ssht00ls/lib/aliases", aliases)
		return r3sponse.success_response(f"Successfully synchronized {c} alias(es).")
	def check(self, alias):
		try: CONFIG["aliases"][alias]
		except KeyError: return r3sponse.error_response(f"Alias [{alias}] does not exist.")
		return r3sponse.success_response(f"Alias [{alias}] exists.")

# initialized objects.
aliases = Aliases()

"""


# --------------------
# SSH Config.

# create an ssh alias for the key.
response = aliases.create(self, 
	# the servers name.
	server="myserver", 
	# the username.
	username="administrator", 
	# the ip of the server.
	ip="0.0.0.0",
	# the port of the server.
	port=22,
	# the path to the private key.
	key="/path/to/mykey/private_key",
	# smart card.
	smart_card=False,)
# if successfull you can use the ssh alias <username>.<server>
# $ ssh <username>.<server>

# create an ssh alias for a smart card.
response = aliases.create(self, 
	# the servers name.
	server="myserver", 
	# the username.
	username="administrator", 
	# the ip of the server.
	ip="0.0.0.0",
	# the port of the server.
	port=22,
	# the path to the private key.
	key=smart_card.path,
	# smart card.
	smart_card=True,)

```


"""
