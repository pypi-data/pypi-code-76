#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# syst3m.
try: import syst3m
except ImportError: 
	if os.path.exists("/usr/bin/pip3"): os.system(f"/usr/bin/pip3 install syst3m --user {OWNER}")
	else: os.system(f"pip3 install syst3m")

# imports.
try: 

	# imports.
	import os, sys, requests, ast, json, pathlib, glob, platform, subprocess, pexpect, random, getpass, time

	# inc imports.
	from fil3s import Files, Formats
	from r3sponse import r3sponse
	import cl1, syst3m, encrypti0n, netw0rk

# download.
except ImportError as e:
	import os
	if os.path.exists("/usr/bin/pip3"): 
		os.system(f"/usr/bin/pip3 install -r {syst3m.defaults.get_source_path(__file__, back=3)}/requirements/requirements.txt --user {os.environ.get('USER')}")
	else:
		os.system(f"pip3 install -r {syst3m.defaults.get_source_path(__file__, back=3)}/requirements/requirements.txt")

	# imports.
	import os, sys, requests, ast, json, pathlib, glob, platform, subprocess, pexpect, random, getpass, time

	# inc imports.
	from fil3s import Files, Formats
	from r3sponse import r3sponse
	import cl1, syst3m, encrypti0n, netw0rk


# source.	
ALIAS = "ssht00ls"
SOURCE_NAME = "ssht00ls"
SOURCE_PATH = syst3m.defaults.get_source_path(__file__, back=3)
BASE = syst3m.defaults.get_source_path(SOURCE_PATH)
OS = syst3m.defaults.check_operating_system(supported=["linux", "osx"])
syst3m.defaults.check_alias(alias=ALIAS, executable=f"{SOURCE_PATH}")

# universal variables.
OWNER = os.environ.get("USER")
GROUP = "root"
HOME_BASE = "/home/"
HOME = f"/home/{os.environ.get('USER')}/"
MEDIA = f"/media/{os.environ.get('USER')}/"
if OS in ["osx"]: 
	HOME_BASE = "/Users/"
	HOME = f"/Users/{os.environ.get('USER')}/"
	MEDIA = f"/Volumes/"
	GROUP = "wheel"

# network.
NETWORK_INFO = netw0rk.network.info()
if not NETWORK_INFO.success: 
	r3sponse.log(error=NETWORK_INFO.error, json=cl1.arguments_present(["--json", "-j"]))
	sys.exit(1)

# check lib.
if not os.path.exists(f"{SOURCE_PATH}/lib"):
	print("Downloading ssht00ls library.")
	os.system(f"rm -fr /tmp/ssht00ls && git clone https://github.com/vandenberghinc/ssht00ls /tmp/ssht00ls && cp -r /tmp/ssht00ls/ssht00ls/lib {SOURCE_PATH}/lib")

# check usr lib.
if not os.path.exists("/usr/local/lib/ssht00ls"):
	print("Installing ssht00ls into system library.")
	os.system(f"rsync -azP {SOURCE_PATH}/ /usr/local/lib/ssht00ls")

# database.
for dir, permission in [
	[f"{HOME}/.{ALIAS}", 770],
	[f"{HOME}/.{ALIAS}/lib", 770],
	[f"{HOME}/.{ALIAS}/.cache", 770],
]:
	if not os.path.exists(dir): os.system(f"sudo mkdir {dir} && sudo chown {OWNER}:{GROUP} {dir} && sudo chmod {permission} {dir}")

# files.
DATABASE = Files.Directory(path=f"{HOME}/.{ALIAS}")
CONFIG = Files.Dictionary(path=syst3m.env.fill(syst3m.env.get_string("SSHT00LS_CONFIG", default=DATABASE.join("config",""))), load=True, default={
	"aliases":{
		"example.com (key's are optional)":{
			"user":"administrator",
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

# universal options.
INTERACTIVE = not cl1.arguments_present(["--non-interactive"])
JSON = cl1.arguments_present(["-j", "--json"])

# initialize cache.
cache = syst3m.cache.Cache(
	path=f"{HOME}/.{ALIAS}/.cache/",)
webserver = syst3m.cache.WebServer(
	path=f"{HOME}/.{ALIAS}/.cache/",
	host="127.0.0.1",
	port=52379,)
if cl1.argument_present("--stop-agent"):
	if not webserver.running(): 
		r3sponse.log(error="The ssht00ls agent is not running.", json=JSON)
		sys.exit(1)
	processes = syst3m.processes(includes="ssht00ls/ --start-agent")
	if not processes.success: 
		r3sponse.log(response=processes, json=json)
		sys.exit(0)
	if len(processes.processes) <= 1:
		r3sponse.log(error="Unable to find the pid of the ssht00ls agent.", json=json)
		sys.exit(0)
	for pid, info in processes.processes.items():
		if info["process"] not in ["grep"]:
			response = syst3m.kill(pid=pid)
			if not response.success: 
				r3sponse.log(response=processes, json=json)
				sys.exit(0)
	r3sponse.log(message="Successfully stopped the ssht00ls agent.", json=json)
	sys.exit(0)
elif cl1.argument_present("--start-agent"):
	if not webserver.running(): 
		webserver.start()
		sys.exit(0)
	else:
		r3sponse.log(error="The ssht00ls agent is already running.", json=JSON)
		sys.exit(1)
else:
	if not cl1.argument_present("--non-interactive") and not webserver.running(): 
		print("Starting the ssht00ls agent.")
		p = subprocess.Popen(["python3", SOURCE_PATH, "--start-agent", "2>", "/dev/null"])
		time.sleep(3)

# encryption.
if None in [CONFIG.dictionary["encryption"]["public_key"], CONFIG.dictionary["encryption"]["private_key"]]:
	if INTERACTIVE:
		passphrase = getpass.getpass("Enter the passphrase of the ssht00ls encryption:")
		if len(passphrase) < 8: 
			r3sponse.log(error="The passphrase must contain at least 8 characters.", json=cl1.arguments_present(["--json", "-j"]))
			sys.exit(1)
		elif passphrase.lower() == passphrase: 
			r3sponse.log(error="The passphrase must contain capital characters.", json=cl1.arguments_present(["--json", "-j"]))
			sys.exit(1)
		elif passphrase != getpass.getpass("Enter the same passphrase:"): 
			r3sponse.log(error="The passphrase must contain at least 8 characters.", json=cl1.arguments_present(["--json", "-j"]))
			sys.exit(1)
		ENCRYPTION = encrypti0n.aes.AsymmetricAES(
			public_key=CONFIG.dictionary["encryption"]["public_key"],
			private_key=CONFIG.dictionary["encryption"]["public_key"],
			passphrase=passphrase,
			memory=True,)
		response = ENCRYPTION.generate_keys()
		if not response["success"]: 
			r3sponse.log(error=f"Encoutered an error while generating the master encryption key: {response['error']}", json=cl1.arguments_present(["--json", "-j"]))
			sys.exit(1)
		ENCRYPTION.rsa.private_key = response.private_key
		ENCRYPTION.rsa.public_key = response.public_key
		CONFIG.dictionary["encryption"]["public_key"] = ENCRYPTION.rsa.public_key
		CONFIG.dictionary["encryption"]["private_key"] = ENCRYPTION.rsa.private_key
		CONFIG.save()
		response = ENCRYPTION.load_keys()
		if not response["success"]: 
			r3sponse.log(error=f"Encoutered an error while activating the ssht00ls encryption: {response['error']}", json=cl1.arguments_present(["--json", "-j"]))
			sys.exit(1)
		response = webserver.set(group="passphrases", id="master", data=passphrase)
		if not response["success"]: 
			r3sponse.log(error=f"Encoutered an error while parsing the webserver: {response['error']}", json=cl1.arguments_present(["--json", "-j"]))
			sys.exit(1)
	#else:
	#	r3sponse.log(error="There is no encryption installed.", json=JSON)
	#	sys.exit(1)
else:
	response, new, passphrase = webserver.get(group="passphrases", id="master"), False, None
	if response["success"]:
		passphrase = response["data"]
	if passphrase == None:
		if not INTERACTIVE:
			r3sponse.log(error=response.error, json=JSON)
			sys.exit(1)
		new = True
		passphrase = getpass.getpass("Enter the passphrase of the ssht00ls encryption:")
	ENCRYPTION = encrypti0n.aes.AsymmetricAES(
		public_key=CONFIG.dictionary["encryption"]["public_key"],
		private_key=CONFIG.dictionary["encryption"]["private_key"],
		passphrase=passphrase,
		memory=True,)
	response = ENCRYPTION.load_keys()
	if not response["success"]: 
		r3sponse.log(error=f"Encoutered an error while activating the ssht00ls encryption: {response['error']}", json=cl1.arguments_present(["--json", "-j"]))
		sys.exit(1)
	if new:
		response = webserver.set(group="passphrases", id="master", data=passphrase)
		if not response["success"]: 
			r3sponse.log(error=f"Encoutered an error while parsing the webserver: {response['error']}", json=cl1.arguments_present(["--json", "-j"]))
			sys.exit(1)

# encrypted database.
ENCRYPTED_DATABASE = encrypti0n.aes.Database(path=f"{HOME}/.{ALIAS}/.cache.enc/", aes=ENCRYPTION)
response = ENCRYPTED_DATABASE.activate()
if not response["success"]: 
	r3sponse.log(error=f"Encoutered an error while parsing the webserver: {response['error']}", json=cl1.arguments_present(["--json", "-j"]))
	sys.exit(1)
PASSPHRASES = ENCRYPTED_DATABASE.load("passphrases")

#