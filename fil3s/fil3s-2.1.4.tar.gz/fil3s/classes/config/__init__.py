#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, sys, requests, ast, json, pathlib, platform, random, shutil, zipfile, pwd, grp, subprocess, time
from datetime import datetime

# fyunctions.
def __get_operating_system__():
	os = platform.system().lower()
	if os in ["darwin"]: return "macos"
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
def __check_alias__(source_name, source_path, version, _os_):
	alias = source_name.lower()
	path = f"/usr/local/bin/{alias}"
	if not os.path.exists(path):
		file = f"""package={SOURCE_PATH}/\nargs=""\nfor var in "$@" ; do\n   	if [ "$args" == "" ] ; then\n   		args=$var\n   	else\n   		args=$args" "$var\n   	fi\ndone\npython3 $package $args\n"""
		os.system(f"sudo touch {path}")
		os.system(f"sudo chmod 755 {path}")
		if _os_ in ["macos"]:
			os.system(f"sudo chown {os.environ.get('USER')}:wheel {path}")
		elif _os_ in ["linux"]:
			os.system(f"sudo chown {os.environ.get('USER')}:root {path}")
		__save_file__(f"{path}", file)
		os.system(f"sudo chmod 755 {path}")
		if '--silent' not in sys.argv:
			print(f'Successfully created alias: {alias}.')
			print(f"Check out the docs for more info $: {alias} -h")

# source.
ALIAS = "fil3s"
SOURCE_NAME = "fil3s"
VERSION = "v1"
SOURCE_PATH, BASE = __get_source_path__(SOURCE_NAME, index=1)
OS = __get_operating_system__()
#__check_alias__(SOURCE_NAME,SOURCE_PATH,VERSION,OS)

# file settings.
OWNER = os.environ.get("USER")
GROUP = "root"
if OS in ["macos"]: GROUP = "wheel"

