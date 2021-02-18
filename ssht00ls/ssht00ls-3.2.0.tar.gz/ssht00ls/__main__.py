#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, sys, syst3m ; sys.path.insert(1, syst3m.defaults.source_path(__file__, back=2))
from ssht00ls.classes.config import *
import ssht00ls

# the cli object class.
class CLI(cl1.CLI):
	def __init__(self):
		
		# defaults.
		cl1.CLI.__init__(self,
			modes={
				"Aliases:":"*chapter*",
				"    --list-aliases":"List all aliases.",
				"        --joiner ','":"Optionally specify the joiner.",
				"    --alias myserver":"Select one or multiple aliases (example x,y,z) (or use * [\\*] for all).",
				"        --info":"Show the aliases info.",
				"        --delete":"Delete an alias.",
				"            -f / --forced":"Ignore the are you sure prompt.",
				"        --create":"Create an alias.",
				"            --server myserver":"Specify the server's name.",
				"            --username myuser":"Specify the username.",
				"            --ip 0.0.0.0":"Specify the server's ip.",
				"            --port 22":"Specify the server's port.",
				"            for ssh keys:":"",
				"            --key /path/to/key/private_key":"Specify the path to the private key.",
				"            --passphrase 'MyPassphrase123'":"Specify the keys pasphrase (optional).",
				"            for smart cards:":"",
				"            --smart-cards":"Enable the smart cards boolean.",
				"            --pin 123456":"Specify the smart cards pin code (optional).",
				"        --edit":"Edit the alias config.",
				"            *** same options as --create ***":"",
				"            --alias newalias":"Rename the alias.",
				"Keys:":"*chapter*",
				"    --generate":"Generate a ssh key.",
				"        --path /keys/mykey/":"Specify the keys directory path.",
				"        --passphrase Passphrase123":"Specify the keys passphrase.",
				"        --comment 'My Key'":"Specify the keys comment.",
				"Sessions:":"*chapter*",
				"    --command <alias> 'ls .'":"Execute a command over ssh.",
				"    --session <alias>":"Start a ssh session.",
				"        --options '' ":"Specify additional ssh options (optional).",
				"Push & pull:":"*chapter*",
				"    --pull <path> <alias>:<remote>":"Pull a file / directory.",
				"        --delete":"Also update the deleted files (optional).",
				"        --safe":"Enable version control.",
				"        --forced":"Enable forced mode.",
				"    --push <alias>:<remote> <path>":"Push a file / directory.",
				"        --delete":"Also update the deleted files (optional).",
				"        --safe":"Enable version control.",
				"        --forced":"Enable forced mode.",
				"Mounts:":"*chapter*",
				"    --mount <alias>:<remote> <path>":"Mount a remote directory.",
				"    --sync <alias>:<remote> <path>":"Synchronize a remote & local directory (similair to --mount except it never unmounts on neither sides).",
				"    --unmount <path>":"Unmount a mounted remote directory.",
				"        --sudo":"Root permission required.",
				"        --forced":"Enable forced mode.",
				"    --index <path> / <alias>:<remote>":"Index the specified path / alias:remote.",
				"Agent:":"*chapter*",
				"    --start-agent":"Start the ssht00ls agent manually.",
				"    --stop-agent":"Stop the ssht00ls agent.",
				"Daemons:":"*chapter*",
				"    --start-daemon <alias>:<remote> <path>":"Start a ssync daemon manually.",
				"    --stop-daemon <path>":"Stop a ssync daemon.",
				"    --list-daemons":"List all daemons & their status.",
				"Basic:":"*chapter*",
				"    --kill <identifier>":"Kill all ssh processes that include the identifier.",
				"    --config":"Edit the ssht00ls configuration file (nano).",
				"    --reset-cache":"Reset the cache directory.",
				"    --version":"Show the ssht00ls version.",
				"    -h / --help":"Show the documentation.",
			},
			options={
				"-j / --json":"Print the response in json format.",
				"--non-interative":"Disable interactive mode.",
				"--no-checks":"Disable the default checks.",
				"--log-level <int>":"Overwrite the default log levels.",
				"--timeout <int>":"Overwrite the default timeout integer value (10)",
				"--reattempts <int>":"Overwrite the default reconnects integer value (3).",
				"--daemon-sleeptime <float>":"Overwrite the default daemon sleeptime float value (0.25).",
			},
			notes={
				"Include config file":"Specify the $SSHT00LS_CONFIG environment variable to use a different ssht00ls config file.",
			},
			alias=ALIAS,
			executable=__file__,
		)

		#
	def start(self):
		
		# check arguments.
		self.arguments.check(exceptions=["--log-level", "--create-alias", "--version"], json=JSON)

		#
		# BASICS
		#

		# help.
		if self.arguments.present(['-h', '--help']):
			self.docs(success=True, json=JSON)

		# version.
		elif self.arguments.present(['--version']):
			print(f"{ALIAS} version:",Files.load(f"{SOURCE_PATH}/.version").replace("\n",""))

		# config.
		elif self.arguments.present('--config'):
			if JSON:
				print(CONFIG.dictionary)
			else:
				os.system(f"nano {CONFIG.file_path.path}")

		# kill ssh processes.
		elif self.arguments.present('--kill'):
			response = ssht00ls.ssh.utils.kill(
				identifier=self.arguments.get("--kill"), 
				sudo=self.arguments.present("--sudo"),)
			self.stop(response=response, json=JSON)

		# reset cache.
		elif self.arguments.present('--reset-cache'):
			path = f"{HOME}/.{ALIAS}/.cache/"
			os.system(f"rm -fr {path}")
			if os.path.exists(path):
				self.stop(error=f"Failed to reset cache {path}.", json=JSON)
			else:
				self.stop(message=f"Successfully resetted cache {path}.", json=JSON)

		#
		# ALIASES
		#

		# list aliases.
		elif self.arguments.present("--list-aliases"):
			array = Files.Array(array=ssht00ls.aliases.list())
			if JSON:
				print(array.array)
			else:
				joiner = self.arguments.get("--joiner", required=False, default="\n")
				print(array.string(joiner=joiner))

		# aliases.
		elif self.arguments.present("--alias"):

			# get alias.
			aliases = self.arguments.get("--alias")
			all = ssht00ls.aliases.list()
			all_str = str(all).replace("'","")
			if aliases in ["*", "all"]: aliases = all
			else: aliases = aliases.split(",")
			
			# iterate.
			info = {}
			for alias in aliases:

				# check existance.
				if not self.arguments.present('--create'):
					response = ssht00ls.aliases.info(alias)
					if not response.success: self.stop(response=response)
					alias_info = response.info

				# show info.
				if self.arguments.present('--info'):
					if JSON:
						info[alias] = {alias:alias_info}
					else:
						print(self.__str_representable__({alias:alias_info}, start_indent=0))

				# delete.
				elif self.arguments.present('--delete'):
					if not self.arguments.present(["-f", "--forced"]) and not syst3m.console.input(f"You are deleting alias [{alias}]. Do you wish to proceed?", yes_no=True):
						self.stop(error="Aborted.")
					response = ssht00ls.aliases.delete(alias=alias)
					self.stop(response=response, json=JSON)

				# set passphrase.
				elif self.arguments.present('--delete'):
					passphrase = self.get_passphrase(required=False)
					if passphrase == None:
						if alias_info["smart_card"]:
							if pin != verify_pin:
								self.stop(error="Passphrases do not match.")
						else:
							passphrase = getpass.getpass(f"Enter a new passphrase for key {alias_info['private_key']}")
							if passphrase != verify_passphrase:
								self.stop(error="Passphrases do not match.")
					response = ssht00ls.aliases.edit(alias=alias, value_exceptions=[None], edits={
						"passphrase":passphrase,
						"pin":pin,
					})
					self.stop(response=response, json=JSON)

				# edit config.
				elif self.arguments.present('--edit'):
					
					# edit alias name.
					if self.arguments.present("--alias", count=2):
						new_alias, success = self.arguments.get("--alias", count=2, chapter="aliases", mode="--edit"), True
						try:
							del CONFIG.dictionary["aliases"][alias]
							CONFIG.dictionary["aliases"][new_alias] = alias_info
							CONFIG.save()
						except: success = False
						if success:
							self.stop(message=f"Successfully renamed alias {alias} to {new_alias}.", json=JSON)
						else:
							self.stop(error=f"Failed to rename alias {alias} to {new_alias}.", json=JSON)

					# edit alias config.
					else:
						response = ssht00ls.aliases.edit( 
							# the alias.
							alias=alias,
							# the edits (dict).
							edits={
								"user":self.arguments.get("--username", required=False, default=None),
								"public_ip":self.arguments.get("--public_ip", required=False, default=None),
								"public_port":self.arguments.get("--public_port", required=False, default=None),
								"private_ip":self.arguments.get("--private_ip", required=False, default=None),
								"private_port":self.arguments.get("--private_port", required=False, default=None),
								"private_key":self.arguments.get("--private_key", required=False, default=None),
								"public_key":self.arguments.get("--public_key", required=False, default=None),
								"passphrase":self.arguments.get("--passphrase", required=False, default=None),
								"smart_card":self.arguments.get("--smart_card", format=bool, required=False, default=None),
								"pin":self.arguments.get("--pin", format=int, required=False, default=None),
							},
							# the key exceptions.
							exceptions=[],
							# the value exceptions.
							value_exceptions=[None],
							# save the edits.
							save=True,)
						self.stop(response=response, json=JSON)

				# create.
				elif self.arguments.present('--create'):
					
					# create an alias for the key.
					if not self.arguments.present('--smart-card'):
						key = self.arguments.get('--private-key')
						response = ssht00ls.aliases.create( 
							# the alias.
							alias=self.arguments.get('--alias', chapter="aliases", mode="--create-alias"), 
							# the username.
							username=self.arguments.get('--username'), chapter="aliases", mode="--create-alias", 
							# the public ip of the server.
							public_ip=self.arguments.get('--public-ip', chapter="aliases", mode="--create-alias"),
							# the public port of the server.
							public_port=self.arguments.get('--public-port', chapter="aliases", mode="--create-alias"),
							# the private ip of the server.
							private_ip=self.arguments.get('--private-ip', chapter="aliases", mode="--create-alias"),
							# the private port of the server.
							private_port=self.arguments.get('--private-port', chapter="aliases", mode="--create-alias"),
							# the path to the private key.
							private_key=private_key,
							# the path to the public key.
							public_key=self.arguments.get('--public-key'),
							# the keys passphrase.
							passphrase=getpass.getpass(f"Enter the passphrase of key [{private_key}]:"),
							# smart card.
							smart_card=False,)

					# create an alias for a smart card.
					else:
						response = ssht00ls.aliases.create( 
							# the alias.
							alias=self.arguments.get('--alias', chapter="aliases", mode="--create-alias"), 
							# the username.
							username=self.arguments.get('--username', chapter="aliases", mode="--create-alias"), 
							# the public ip of the server.
							public_ip=self.arguments.get('--public-ip', chapter="aliases", mode="--create-alias"),
							# the public port of the server.
							public_port=self.arguments.get('--public-port', chapter="aliases", mode="--create-alias"),
							# the private ip of the server.
							private_ip=self.arguments.get('--private-ip', chapter="aliases", mode="--create-alias"),
							# the private port of the server.
							private_port=self.arguments.get('--private-port', chapter="aliases", mode="--create-alias"),
							# the path to the private key.
							private_key=ssht00ls.smart_card.path,
							# smart card.
							smart_card=True,
							pin=self.arguments.get('--pin', required=False, default=None, chapter="aliases", mode="--create-alias"), )

					# log to console.
					self.stop(response=response, json=JSON)

				# invalid.
				else: self.invalid(chapter="aliases", json=JSON)

			# json show info joined.
			if JSON and self.arguments.present('--info'):
				print(info)

		#
		# KEYS
		#

		# generate key.
		elif self.arguments.present('--generate'):
			
			# generate a key.
			passphrase = self.get_passphrase(required=False)
			if passphrase in ["", None, "null", "None", "none"]: passphrase = None
			response = ssht00ls.key.generate(
				path=self.arguments.get("--path", chapter="keys", mode="--generate"), 
				passphrase=passphrase, 
				comment=self.arguments.get("--comment", chapter="keys", mode="--generate"),)
			self.stop(response=response, json=JSON)

		#
		# PULL & PUSH
		#

		# pull.
		elif self.arguments.present('--pull'):
			remote = self.arguments.get("--pull", index=1, chapter="push & pull", mode="--pull")
			path = self.arguments.get("--pull", index=2, chapter="push & pull", mode="--pull")
			if ":" not in remote:
				self.docs(
					error=f"Invalid <alias>:<remote> <path> format.", 
					chapter="push & pull", 
					mode="--pull", 
					notes={
						"<alias>:<path>":"Pack the alias & tuple together as one argument in the following format [<alias>:<path>]."
					},
					json=JSON,)
			alias,remote = remote.split(":")
			remote = syst3m.env.fill(remote)
			path = syst3m.env.fill(path)
			exclude = None
			if self.arguments.present("--exclude"): 
				exclude = self.arguments.get("--exclude", chapter="push & pull", mode="--pull").split(",")
			elif self.arguments.present("--no-exclude"): exclude = []
			response = ssht00ls.ssync.pull(
				alias=alias, 
				remote=remote, 
				path=path,
				exclude=exclude, 
				forced=self.arguments.present("--forced"), 
				delete=self.arguments.present("--delete"), 
				safe=self.arguments.present("--safe"), 
				directory=True, )
			self.stop(response=response, json=JSON)

		# push.
		elif self.arguments.present('--push'):
			path = self.arguments.get("--push", index=1, chapter="push & pull", mode="--push")
			remote = self.arguments.get("--push", index=2, chapter="push & pull", mode="--push")
			if ":" not in remote:
				self.docs(
					error=f"Invalid <alias>:<remote> <path>.", 
					chapter="push & pull", 
					mode="--push", 
					notes={
						"<alias>:<path>":"Pack the alias & tuple together as one argument in the following format [<alias>:<path>]."
					},
					json=JSON,)
			alias,remote = remote.split(":")
			remote = syst3m.env.fill(remote)
			path = syst3m.env.fill(path)
			exclude = None
			if self.arguments.present("--exclude"): 
				exclude = self.arguments.get("--exclude", chapter="push & pull", mode="--push").split(",")
			elif self.arguments.present("--no-exclude"): exclude = []
			response = ssht00ls.ssync.push(
				alias=alias, 
				remote=remote, 
				path=path,
				exclude=exclude, 
				forced=self.arguments.present("--forced"), 
				delete=self.arguments.present("--delete"), 
				safe=self.arguments.present("--safe"), 
				directory=True, )
			self.stop(response=response, json=JSON)

		#
		# MOUNTS
		#

		# mount.
		elif self.arguments.present('--mount'):
			remote = self.arguments.get("--mount", index=1, chapter="mounts", mode="--mount", notes={})
			path = self.arguments.get("--mount", index=2, chapter="mounts", mode="--mount", notes={})
			if ":" not in remote:
				self.docs(
					error=f"Invalid <alias>:<remote> <path>.", 
					chapter="mounts", 
					mode="--mount", 
					notes={
						"<alias>:<path>":"Pack the alias & tuple together as one argument in the following format [<alias>:<path>]."
					},
					json=JSON,)
			alias,remote = remote.split(":")
			remote = syst3m.env.fill(remote)
			path = syst3m.env.fill(path)
			response = ssht00ls.ssync.mount(
				alias=alias, 
				remote=remote, 
				path=path,
				forced=self.arguments.present("--forced"), )
			self.stop(response=response, json=JSON)

		# sync.
		elif self.arguments.present('--sync'):
			remote = self.arguments.get("--sync", index=1, chapter="mounts", mode="--sync", notes={})
			path = self.arguments.get("--sync", index=2, chapter="mounts", mode="--sync", notes={})
			if ":" not in remote:
				self.docs(
					error=f"Invalid <alias>:<remote> <path>.", 
					chapter="mounts", 
					mode="--sync", 
					notes={
						"<alias>:<path>":"Pack the alias & tuple together as one argument in the following format [<alias>:<path>]."
					},
					json=JSON,)
			alias,remote = remote.split(":")
			remote = syst3m.env.fill(remote)
			path = syst3m.env.fill(path)
			response = ssht00ls.ssync.mount(
				alias=alias, 
				remote=remote, 
				path=path,
				forced=self.arguments.present("--forced"), 
				mode="sync",)
			self.stop(response=response, json=JSON)

		# unmount.
		elif self.arguments.present('--unmount'):
			path = self.arguments.get("--unmount", index=1, chapter="mounts", mode="--unmount")
			response = ssht00ls.ssync.unmount(
				path=path,
				forced=self.arguments.present("--forced"), 
				sudo=self.arguments.present("--sudo"), )
			self.stop(response=response, json=JSON)

		# index.
		elif self.arguments.present('--index'):
			index = self.arguments.get("--index", chapter="mounts", mode="--index")
			if ":" in index:
				alias,remote = index.split(":")
				path = syst3m.env.fill(path)
				response = ssht00ls.ssync.index(path=remote, alias=alias)
			else:
				path = syst3m.env.fill(path)
				response = ssht00ls.ssync.index(path=index)
			self.stop(response=response, json=JSON)

		#
		# DAEMONS
		#

		# start daemon.
		elif self.arguments.present('--start-daemon'):
			remote = self.arguments.get("--start-daemon", index=1, chapter="daemons", mode="--start-daemon")
			path = self.arguments.get("--start-daemon", index=2, chapter="daemons", mode="--start-daemon")
			if ":" not in remote:
				self.docs(
					error=f"Invalid <alias>:<remote> <path>.", 
					chapter="damons", 
					mode="--start-daemon", 
					notes={
						"<alias>:<path>":"Pack the alias & tuple together as one argument in the following format [<alias>:<path>]."
					},
					json=JSON,)
			alias,remote = remote.split(":")
			remote = syst3m.env.fill(remote)
			path = syst3m.env.fill(path)
			response = ssht00ls.ssync.daemon(alias=alias, remote=remote, path=path)
			self.stop(response=response, json=JSON)

		# stop daemon.
		elif self.arguments.present('--stop-daemon'):
			c = 0
			for path in self.arguments.get("--stop-daemon", index=1, chapter="daemon", mode="--stop-daemon", format=list):
				response = ssht00ls.ssync.daemons.stop(path)
				if not response["success"]:
					self.stop(response=response, json=JSON)
					c += 1
			if c > 0:
				self.stop(message=f"Successfully stopped {c} daemon(s).", json=JSON)
			else:
				self.stop(error="No daemons found.", json=JSON)

		# list daemons.
		elif self.arguments.present('--list-daemons'):
			
			daemons = ssht00ls.ssync.daemons.status()
			if len(daemons) == 0:
				self.stop(message=f"There are no active daemons.", json=JSON)
			print("Daemons:")
			for path, status in daemons.items():
				print(f" * {path}: {status}")
			self.stop(message=f"Successfully listed {len(daemons)} daemon(s).", json=JSON)

		# invalid.
		else: self.invalid()

		#
	def get_passphrase(self, required=True):
		passphrase = self.arguments.get("--passphrase", required=required)
		if passphrase != None: return passphrase.replace("\\", "").replace("\ ", "")
		else: return passphrase
# main.
if __name__ == "__main__":
	cli = CLI()
	cli.start()
