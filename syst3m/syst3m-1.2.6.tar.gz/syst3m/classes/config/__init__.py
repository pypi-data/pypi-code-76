#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, sys, requests, ast, json, pathlib, glob, platform, subprocess, time, random, threading, urllib, flask, logging, multiprocessing

# inc imports.
import cl1
from fil3s import Files, Formats
from r3sponse import r3sponse

# fyunctions.
def __get_operating_system__():
	os = platform.system().lower()
	if os in ["darwin"]: return "osx"
	elif os in ["linux"]: return "linux"
	else: raise ValueError(f"Unsupported operating system: [{os}].")
def __get_source_path__(package_name, index=1):
	executive_dir = str(pathlib.Path(__file__).absolute()).replace(os.path.basename(pathlib.Path(__file__)), '').replace("//","/")
	if executive_dir[len(executive_dir)-1] == "/": executive_dir = executive_dir[:-1]
	source, c = "/", 1
	for id in executive_dir.split("/"):
		if id == package_name:
			if c == index:
				source += id+"/"
				break
			else: c += 1
		else: source += id+"/"
	base = source[:-1].split("/")
	base = source.replace(f'/{base[len(base)-1]}/', '/')
	return source, base
def __save_file__(path, data):
	file = open(path, "w+") 
	file.write(data)
	file.close()
def __check_alias__(
	# the source name.
	alias=None, 
	# the source path.
	executable=None,
):
	present = "--create-alias" in sys.argv and cl1.get_argument("--create-alias") == alias
	base = f"/usr/local/bin"
	if not os.path.exists(base):
		base = f"/usr/bin/"
	path = f"{base}/{alias}"
	if present or not os.path.exists(path):
		file = f"""#!/usr/bin/env python3\nimport os, sys\npackage="{executable}"\nsys.argv.pop(0)\narguments = sys.argv\ns = ""\nfor i in arguments:\n	if s == "": \n		if " " in i: s = "'"+i+"'"\n		else: s = i\n	else: \n		if " " in i: s += " '"+i+"'"\n		else: s += " "+i\nos.system("python3 "+package+" "+s)"""

		os.system(f"touch {path}")
		os.system(f"chmod +x {path}")
		os.system(f"chown {USER}:{GROUP} {path}")
		try:
			Files.File(path=f"{path}", data=file).save()
		except:
			print(f"Unable to create alias $ {alias}.")
			return None
		os.system(f"chmod +x {path}")
		if '--silent' not in sys.argv:
			print(f'Successfully created alias: {alias}.')
			print(f"Check out the docs for more info $: {alias} -h")
	if present:
		quit()

# source.
ALIAS = "syst3m"
SOURCE_NAME = "syst3m"
SOURCE_PATH= Formats.FilePath(__file__).base(back=3)
OS = __get_operating_system__()

# universal variables.
USER = os.environ.get("USER")
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

# check alias.
__check_alias__(SOURCE_NAME,f"{SOURCE_PATH}")