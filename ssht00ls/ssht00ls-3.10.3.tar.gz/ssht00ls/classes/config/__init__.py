#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# alias.
ALIAS = "ssht00ls"

# updates.
import os, sys
try: import cl1
except ImportError: 
	if os.path.exists("/usr/bin/pip3"): os.system(f"/usr/bin/pip3 install cl1 --user {OWNER}")
	else: os.system(f"pip3 install cl1")
	import cl1
if cl1.arguments_present(["--update"]):
	os.system(f"curl -s https://raw.githubusercontent.com/vandenberghinc/{ALIAS}/master/{ALIAS}/requirements/installer.remote | bash ")
	sys.exit(0)

# imports.
try: 

	# imports.
	import os, sys, requests, ast, json, pathlib, glob, platform, subprocess, pexpect, random, getpass, time

	# inc imports.
	from fil3s import *
	from r3sponse import r3sponse
	import cl1, syst3m, encrypti0n, netw0rk

# download.
except ImportError as e:
	import os
	if os.path.exists("/usr/bin/pip3"): 
		os.system(f"/usr/bin/pip3 install -r {syst3m.defaults.source_path(__file__, back=3)}/requirements/requirements.txt --user {os.environ.get('USER')}")
	else:
		os.system(f"pip3 install -r {syst3m.defaults.source_path(__file__, back=3)}/requirements/requirements.pip")

	# imports.
	import os, sys, requests, ast, json, pathlib, glob, platform, subprocess, pexpect, random, getpass, time

	# inc imports.
	from fil3s import *
	from r3sponse import r3sponse
	import cl1, syst3m, encrypti0n, netw0rk


# source.	
SOURCE_PATH = syst3m.defaults.source_path(__file__, back=3)
BASE = syst3m.defaults.source_path(SOURCE_PATH)
OS = syst3m.defaults.operating_system(supported=["linux", "macos"])
LOG_LEVEL = syst3m.defaults.log_level(default=0)
syst3m.defaults.alias(alias=ALIAS, executable=f"{SOURCE_PATH}")

# universal options.
CLI = syst3m.env.get_boolean("CLI")
INTERACTIVE = not cl1.arguments_present(["--non-interactive"]) and not syst3m.env.get_boolean("NON_INTERACTIVE")
CHECKS = not cl1.arguments_present(["--no-checks"])
JSON = cl1.arguments_present(["-j", "--json"])

# version.
try: version = Files.load(f"{SOURCE_PATH}/.version")
except: version = "unkown"

# universal variables.
USER = OWNER = os.environ.get("USER")
GROUP = "root"
HOME_BASE = "/home/"
HOME = f"/home/{USER}/"
MEDIA = f"/media/{USER}/"
if OS in ["macos"]: 
	HOME_BASE = "/Users/"
	HOME = f"/Users/{USER}/"
	MEDIA = f"/Volumes/"
	GROUP = "wheel"

# initialize cache.
cache = syst3m.cache.Cache(
	path=f"{HOME}/.{ALIAS}/.cache/",)

# files.
DATABASE = Files.Directory(path=f"{HOME}/.{ALIAS}")
CONFIG = Dictionary(path=syst3m.env.fill(syst3m.env.get_string("SSHT00LS_CONFIG", default=DATABASE.join("config",""))), load=True, default={})

# netw0rk settings.
IPINFO_API_KEY = os.environ.get("IPINFO_API_KEY")

# ssh settings.
SSH_TIMEOUT = int(cl1.get_argument("--timeout", required=False, default=10))
SSH_REATTEMPS = int(cl1.get_argument("--reattempts", required=False, default=3))
DEFAULT_SSH_OPTIONS = f"-o ConnectTimeout={SSH_TIMEOUT} -o ConnectionAttempts={SSH_REATTEMPS}"

# daemon settings.
SSYNC_DAEMON_SLEEPTIME = round(float(cl1.get_argument("--daemon-sleeptime", required=False, default=0.25)), 2)

# speed up non interactive.
if CHECKS and not cl1.arguments_present("--reset-cache"):

	# network.
	NETWORK_INFO = netw0rk.network.info()
	if not NETWORK_INFO["success"]: 
		r3sponse.log(error=NETWORK_INFO.error, json=cl1.arguments_present(["--json", "-j"]), log_level=0)
		sys.exit(1)

	# check lib.
	if not Files.exists(f"{SOURCE_PATH}/lib"):
		r3sponse.log("Downloading the ssht00ls library.")
		os.system(f"rm -fr /tmp/ssht00ls && git clone https://github.com/vandenberghinc/ssht00ls /tmp/ssht00ls && rsync -azq /tmp/ssht00ls/ssht00ls/lib/ {SOURCE_PATH}/lib/")

	# check usr lib.
	if not Files.exists("/usr/local/lib/ssht00ls"):
		r3sponse.log(f"{syst3m.color.orange}Root permission{syst3m.color.end} required to install the ssht00ls system library.")
		os.system(f" sudo rsync -azq --delete {SOURCE_PATH}/ /usr/local/lib/ssht00ls")
		Files.chown("/usr/local/lib/ssht00ls", owner=syst3m.defaults.vars.owner, group=syst3m.defaults.vars.group, sudo=True, recursive=True)
		Files.chmod("/usr/local/lib/ssht00ls", permission=770, sudo=True, recursive=True)

	# database.
	for dir, permission in [
		[f"{HOME}/.{ALIAS}", 770],
		[f"{HOME}/.{ALIAS}/lib", 770],
		[f"{HOME}/.{ALIAS}/.cache", 770],
	]:
		if not Files.exists(dir): os.system(f"sudo mkdir {dir} && sudo chown {OWNER}:{GROUP} {dir} && sudo chmod {permission} {dir}")

	# files.
	CONFIG.check(default={
		"aliases":{
			"example.com (key's are optional)":{
				"username":"administrator",
				"public_ip":"192.168.1.100",
				"public_port":22,
				"private_ip":"84.84.123.192",
				"private_port":22,
				"private_key":"~/keys/example.com/administrator/private_key",
				"public_key":"~/keys/example.com/administrator/public_key",
				"passphrase":None,
				"smart_card":False,
				"pin":None,
			}
		},
		"settings": {
			"keep_alive":60,
		},
		"encryption": {
			"public_key":None,
			"private_key":None,
		},
	})

	# limit webserver recursive import.
	if not syst3m.env.get("SSHT00LS_WEBSERVER_IMPORT", format=bool):

		# webserver.
		from ssht00ls.classes.webserver import WebServer
		webserver = WebServer()
		if cl1.argument_present("--stop-agent"):
			response = webserver.stop()
			if response.success:
				r3sponse.log(response=response, json=syst3m.defaults.options.json)
				sys.exit(0)
			else:
				r3sponse.log(response=response, json=syst3m.defaults.options.json)
				sys.exit(1)
		elif cl1.argument_present("--start-agent"):
			if not webserver.running(): 
				webserver.start()
				sys.exit(0)
			else:
				r3sponse.log(error=f"The {webserver.id} is already running.", json=syst3m.defaults.options.json)
				sys.exit(1)
		elif INTERACTIVE and not webserver.running(): 
			response = webserver.fork()
			r3sponse.log(response=response, json=syst3m.defaults.options.json)
			if not response.success: sys.exit(0)

		# encryption.
		from ssht00ls.classes import encryption as _encryption_
		encryption = _encryption_.Encryption(
			config=CONFIG,
			webserver=webserver,
			cache=f"{syst3m.defaults.vars.home}/.{ALIAS}/.cache.enc/",
			interactive=INTERACTIVE,)

		# generate.
		if not INTERACTIVE:
			if None in [CONFIG.dictionary["encryption"]["public_key"], CONFIG.dictionary["encryption"]["private_key"]]:
				if CLI:
					response = encryption.generate()
					r3sponse.log(response=response, json=syst3m.defaults.options.json)
					if not response.success: sys.exit(1)
				else:
					r3sponse.log(error="There is no encryption installed.", json=syst3m.defaults.options.json)
					sys.exit(1)

			# activate.
			else:

				# activate encryption.
				response = encryption.activate()
				r3sponse.log(response=response, json=syst3m.defaults.options.json)
				if not response.success: sys.exit(1)

