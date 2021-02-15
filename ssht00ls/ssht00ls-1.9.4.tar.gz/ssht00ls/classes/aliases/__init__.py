#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from ssht00ls.classes.config import *
from ssht00ls.classes import utils
from ssht00ls.classes.agent import agent

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
		# the path to the private & public key.
		private_key=None,
		public_key=None,
		# the keys passphrase.
		passphrase=None,
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
			try:username = serialized["user"]
			except KeyError: username = None
			try:public_ip = serialized["public_ip"]
			except KeyError: public_ip = None
			try:private_ip = serialized["private_ip"]
			except KeyError: private_ip = None
			try:public_port = serialized["public_port"]
			except KeyError: public_port = None
			try:private_port = serialized["private_port"]
			except KeyError: private_port = None
			try:private_key = serialized["private_key"]
			except KeyError: private_key = None
			try:public_key = serialized["public_key"]
			except KeyError: public_key = None
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
			"private_key":private_key,
			"public_key":public_key,
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
		private_key = syst3m.env.fill(private_key)
		public_key = syst3m.env.fill(public_key)
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
		json_config["public_key"] = public_key
		if not smart_card:
			json_config["private_key"] = private_key
			json_config["smart_card"] = False
			config += "\n    IdentityFile {}".format(private_key)
		else:
			json_config["private_key"] = smart_cards.path
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
				response = ENCRYPTION.encrypt(str(passphrase))
				if not response["success"]: return response
				CONFIG["aliases"][alias]["passphrase"] = response["encrypted"].decode()
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
		for alias in list(CONFIG["aliases"].keys()):
			info = CONFIG["aliases"][alias]
			if "example.com " not in alias:
				checked = Files.Dictionary(path=False, dictionary=info).check(default={
					"user":None,
					"public_ip":None,
					"private_ip":None,
					"public_port":None,
					"private_port":None,
					"private_key":None,
					"public_key":None,
					"passphrase":None,
					"smart_card":None,
					"pin":None,
				})
				if isinstance(checked["private_key"], str):
					checked["private_key"] = syst3m.env.fill(checked["private_key"])
				if isinstance(checked["public_key"], str):
					checked["public_key"] = syst3m.env.fill(checked["public_key"])
				if not cl1.argument_present("--non-interactive"):
					passphrase = None
					if checked["smart_card"] and checked["pin"] in [None, "", "none", "None"]:
						passphrase =  getpass.getpass(f"Enter the passphrase of key {checked['key']}:")
					elif checked["passphrase"] in [None, "", "none", "None"]:
						passphrase =  getpass.getpass(f"Enter the passphrase of key {checked['key']}:")
					if checked["smart_card"]:
						response = agent.check(public_key=checked["public_key"], raw=True)
					else:
						response = agent.check(public_key=checked["public_key"], raw=False)
					if not response["success"]:
						if "is not added" not in response["error"]: return response
						elif "is not added" in response["error"]:
							if checked["smart_card"]:
								response = agent.add(path=checked["private_key"], smart_card=True, pin=passphrase)
								if not response["success"]: return response
							else:
								response = agent.add(path=checked["private_key"], passphrase=passphrase)
								if not response["success"]: return response
					if passphrase != None:
						response = ENCRYPTION.encrypt(passphrase)
						if not response.success: return response
						if checked["smart_card"]:
							CONFIG["aliases"][alias]["pin"] = response.encrypted.decode()
						else:
							CONFIG["aliases"][alias]["passphrase"] = response.encrypted.decode()
						CONFIG.save()
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
