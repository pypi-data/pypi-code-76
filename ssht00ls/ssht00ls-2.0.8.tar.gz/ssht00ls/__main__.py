#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, sys, syst3m ; sys.path.insert(1, syst3m.defaults.get_source_path(__file__, back=2))
from ssht00ls.classes.config import *
import ssht00ls

# the cli object class.
class CLI(cl1.CLI):
	def __init__(self):
		
		# defaults.
		cl1.CLI.__init__(self,
			modes={
				"--create-alias":"Create a ssh alias.",
				"    --server myserver":"Specify the server's name.",
				"    --username myuser":"Specify the username.",
				"    --ip 0.0.0.0":"Specify the server's ip.",
				"    --port 22":"Specify the server's port.",
				"    for ssh keys:":"",
				"    --key /path/to/key/private_key":"Specify the path to the private key.",
				"    --passphrase 'MyPassphrase123'":"Specify the keys pasphrase (optional).",
				"    for smart cards:":"",
				"    --smart-cards":"Enable the smart cards boolean.",
				"    --pin 123456":"Specify the smart cards pin code (optional).",
				"--generate":"Generate a ssh key.",
				"    --path /keys/mykey/":"Specify the keys directory path.",
				"    --passphrase Passphrase123":"Specify the keys passphrase.",
				"    --comment 'My Key'":"Specify the keys comment.",
				"--command <alias> 'ls .'":"Execute a command over ssh.",
				"--session <alias>":"Start a ssh session.",
				"    --options '' ":"Specify additional ssh options (optional).",
				"--pull <path> <alias>:<remote>":"Pull a file / directory.",
				"    --delete":"Also update the deleted files (optional).",
				"    --safe":"Enable version control.",
				"    --forced":"Enable forced mode.",
				"--push <alias>:<remote> <path>":"Push a file / directory.",
				"    --delete":"Also update the deleted files (optional).",
				"    --safe":"Enable version control.",
				"    --forced":"Enable forced mode.",
				"--mount <alias>:<remote> <path>":"Mount a remote directory.",
				"--unmount <path>":"Unmount a mounted remote directory.",
				"    --sudo":"Root permission required.",
				"    --forced":"Enable forced mode.",
				"--index <path> / <alias>:<remote>":"Index the specified path / alias:remote.",
				"--start-agent":"Start the ssht00ls agent.",
				"--stop-agent":"Stop the ssht00ls agent.",
				"--start-daemon <alias>:<remote> <path>":"Start a ssync daemon.",
				"--stop-daemon <path>":"Stop a ssync daemon.",
				"--kill <identifier>":"Kill all ssh processes that include the identifier.",
				"--config":"Edit the ssht00ls configuration file (nano).",
				"-h / --help":"Show the documentation.",
			},
			options={
				"-j / --json":"Print the response in json format.",
			},
			notes={
				"SSHT00LS_CONFIG":"Specify the $SSHT00LS_CONFIG environment variable to use a different ssht00ls config file.",
			},
			alias=ALIAS,
			executable=__file__,
		)

		#
	def start(self):
		
		# help.
		if self.arguments_present(['-h', '--help']):
			print(self.documentation)

		# check create ssh config.
		elif self.argument_present('--create-alias'):
			
			# create an ssh alias for the key.
			if not self.argument_present('--smart-card'):
				key = self.get_argument('--key')
				response = ssht00ls.aliases.create( 
					# the alias.
					alias=self.get_argument('--alias'), 
					# the username.
					username=self.get_argument('--username'), 
					# the public ip of the server.
					public_ip=self.get_argument('--public-ip'),
					# the public port of the server.
					public_port=self.get_argument('--public-port'),
					# the private ip of the server.
					private_ip=self.get_argument('--private-ip'),
					# the private port of the server.
					private_port=self.get_argument('--private-port'),
					# the path to the private key.
					key=key,
					passphrase=getpass.getpass("Enter the passphrase of key [{key}]:"),
					# smart card.
					smart_card=False,)

			# create an ssh alias for a smart card.
			else:
				response = ssht00ls.aliases.create( 
					# the alias.
					alias=self.get_argument('--alias'), 
					# the username.
					username=self.get_argument('--username'), 
					# the public ip of the server.
					public_ip=self.get_argument('--public-ip'),
					# the public port of the server.
					public_port=self.get_argument('--public-port'),
					# the private ip of the server.
					private_ip=self.get_argument('--private-ip'),
					# the private port of the server.
					private_port=self.get_argument('--private-port'),
					# the path to the private key.
					key=smart_card.path,
					# smart card.
					smart_card=True,
					pin=self.get_argument('--pin', required=False, default=None), )

			# log to console.
			r3sponse.log(response=response, json=JSON)

		# check create ssh config.
		elif self.argument_present('--generate'):
			
			# generate a key.
			passphrase = self.get_passphrase(required=False)
			if passphrase in ["", None, "null", "None", "none"]: passphrase = None
			response = ssht00ls.key.generate(
				path=self.get_argument("--path"), 
				passphrase=passphrase, 
				comment=self.get_argument("--comment"),)
			r3sponse.log(response=response, json=JSON)

		# kill ssh processes.
		elif self.argument_present('--kill'):
			response = ssht00ls.utils.kill_ssh(
				identifier=self.get_argument("--kill"), 
				sudo=self.argument_present("--sudo"),)
			r3sponse.log(response=response, json=JSON)

		# pull.
		elif self.argument_present('--pull'):
			remote = self.get_argument("--pull", index=1)
			path = self.get_argument("--pull", index=2)
			if ":" not in remote:
				r3sponse.log(error=f"Invalid <alias>:<remote> <path> format.", json=JSON)
				self.stop()
			alias,remote = remote.split(":")
			exclude = None
			if self.argument_present("--exclude"): 
				exclude = self.get_argument("--exclude").split(",")
			elif self.argument_present("--no-exclude"): exclude = []
			response = ssht00ls.ssync.pull(
				alias=alias, 
				remote=remote, 
				path=path,
				exclude=exclude, 
				forced=self.argument_present("--forced"), 
				delete=self.argument_present("--delete"), 
				safe=self.argument_present("--safe"), )
			r3sponse.log(response=response, json=JSON)

		# push.
		elif self.argument_present('--push'):
			path = self.get_argument("--push", index=1)
			remote = self.get_argument("--push", index=2)
			if ":" not in remote:
				r3sponse.log(error=f"Invalid <alias>:<remote> <path>.", json=JSON)
				self.stop()
			alias,remote = remote.split(":")
			exclude = None
			if self.argument_present("--exclude"): 
				exclude = self.get_argument("--exclude").split(",")
			elif self.argument_present("--no-exclude"): exclude = []
			response = ssht00ls.ssync.push(
				alias=alias, 
				remote=remote, 
				path=path,
				exclude=exclude, 
				forced=self.argument_present("--forced"), 
				delete=self.argument_present("--delete"), 
				safe=self.argument_present("--safe"), )
			r3sponse.log(response=response, json=JSON)

		# mount.
		elif self.argument_present('--mount'):
			remote = self.get_argument("--mount", index=1)
			path = self.get_argument("--mount", index=2)
			if ":" not in remote:
				r3sponse.log(error=f"Invalid <alias>:<remote> <path>.", json=JSON)
				self.stop()
			alias,remote = remote.split(":")
			response = ssht00ls.ssync.mount(
				alias=alias, 
				remote=remote, 
				path=path,
				forced=self.argument_present("--forced"), )
			r3sponse.log(response=response, json=JSON)

		# unmount.
		elif self.argument_present('--unmount'):
			path = self.get_argument("--unmount", index=1)
			response = ssht00ls.ssync.unmount(
				path=path,
				forced=self.argument_present("--forced"), 
				sudo=self.argument_present("--sudo"), )
			r3sponse.log(response=response, json=JSON)

		# index.
		elif self.argument_present('--index'):
			index = self.get_argument("--index")
			if ":" in index:
				alias,remote = index.split(":")
				response = ssht00ls.ssync.index(path=remote, alias=alias)
			else:
				response = ssht00ls.ssync.index(path=index)
			r3sponse.log(response=response, json=JSON)

		# start daemon.
		elif self.argument_present('--start-daemon'):
			remote = self.get_argument("--start-daemon", index=1)
			path = self.get_argument("--start-daemon", index=2)
			if ":" not in remote:
				r3sponse.log(error=f"Invalid <alias>:<remote> <path>.", json=JSON)
				self.stop()
			alias,remote = remote.split(":")
			response = ssht00ls.ssync.daemon(alias=alias, remote=remote, path=path)
			r3sponse.log(response=response, json=JSON)

		# stop daemon.
		elif self.argument_present('--stop-daemon'):
			path = self.get_argument("--stop-daemon", index=1)
			response = ssht00ls.ssync.stop_daemon(path)
			r3sponse.log(response=response, json=JSON)

		# config.
		elif self.argument_present('--config'):
			if json:
				print(CONFIG.dictionary)
			else:
				os.system(f"nano {CONFIG.file_path.path}")

		# invalid.
		else: self.invalid()

		#
	def invalid(self):
		if JSON:
			r3sponse.log(error="Selected an invalid mode.", json=JSON)
		else:
			print(self.documentation)
			print("Selected an invalid mode.")
		#
	def stop(self, success=False):
		if success: sys.exit(1)
		else:sys.exit(1)
	def get_passphrase(self, required=True):
		return self.get_argument("--passphrase", required=required).replace("\\", "").replace("\ ", "")
# main.
if __name__ == "__main__":
	cli = CLI()
	cli.start()
