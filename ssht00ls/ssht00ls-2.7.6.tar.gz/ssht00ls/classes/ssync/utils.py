#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os
from fil3s import Files, Formats, gfp
from r3sponse import r3sponse
from ssht00ls.classes.config import * 
from ssht00ls.classes import utils

# settings.
INCLUDE = ['.git', 'dist', "'*.egg-info'"]
EXCLUDE = ['__pycache__', '.DS_Store']

# serialize path.
def serialize_path(path, append_last_slash=False):
	# keep in mind the file is saved by python and then executed.
	list = []
	for i in [" ","!","?","@","#","$","&","(",")","[","]","{","}"]:
		list.append([i, f"\\{i}"],)
	for x,y in list+[
		#[" ", "\\ "],
	]:
		path = path.replace(x,y)
	while True:
		if append_last_slash and len(path) > 0 and path[len(path)-1] == "/": path = path[:-1]
		else: break
	return path

# index.
def index(path):
	index, dir, ids = Files.Dictionary(path=False, dictionary={}), Files.Directory(path=path), []
	for _path_ in dir.paths(recursive=True, files_only=True, banned=[gfp.clean(f"{path}/Icon\r")], banned_names=[".DS_Store", "__pycache__"]):
		if _path_ not in ids: 
			index[_path_] = gfp.mtime(path=_path_, format="seconds")
			ids.append(_path_)
	for _path_ in dir.paths(recursive=True, dirs_only=True, banned=[gfp.clean(f"{path}/Icon\r")], banned_names=[".DS_Store", "__pycache__"]):
		id = _path_+" (d)"
		if os.listdir(_path_) == []: id += " (e)"
		if id not in ids: 
			index[id] = gfp.mtime(path=_path_, format="seconds")
			ids.append(id)
	return index.sort(alphabetical=True)

# pull.
def pull(
	# the local path.
	path=None, 
	# the ssht00ls alias.
	alias=None, 
	# the remote path.
	remote=None, 
	# exlude subpaths (list) (leave None to use default).
	exclude=None,
	# include subpaths (list) (leave None to use default).
	include=None,
	# path is directory boolean (leave None to parse automatically).
	directory=True,
	empty_directory=False,
	# update deleted files.
	delete=False,
	# forced mode.
	forced=False,
	# version control.
	safe=False,
	# accept new hosts keys.
	accept_new_host_keys=True,
	# checks.
	checks=True,
	# log level.
	log_level=0,
	# get the command in str.
	command=False,
):	
	# checks.
	if exclude == None: exclude = EXCLUDE
	if include == None: include = INCLUDE
	if checks:

		# check alias.
		path = serialize_path(gfp.clean(path))
		remote = serialize_path(gfp.clean(remote))
		#response = aliases.check(alias)
		#if not response.success: return response
		
		# check passphrase.
		#if CONFIG["aliases"][alias]["smart_card"] in [True, "true", "True"]:
		#	response = ENCRYPTION.decrypt(CONFIG["aliases"][alias]["passphrase"])
		#else:
		#	response = ENCRYPTION.decrypt(CONFIG["aliases"][alias]["passphrase"])
		#if not response.success: return response
		#passphrase = response.decrypted.decode()
		
		# tests.
		#response = agent.add(path=CONFIG["aliases"][alias]["private_key"], passphrase=passphrase)
		#if not response["success"]: return response
		response = utils.test_ssht00ls(alias=alias, accept_new_host_keys=accept_new_host_keys)
		if not response.success: return response
		response = utils.test_ssh_path(alias=alias, path=remote, accept_new_host_keys=accept_new_host_keys)
		if not response.success: return response

		# dir.
		if directory == None: 
			response = utils.test_ssh_dir(alias=alias, path=remote, accept_new_host_keys=accept_new_host_keys)
			if not response.success and "not a directory" not in response.error: return response
			elif response.success:
				directory = True
			else: directory = False
			tested = True
		elif directory:
			response = utils.test_ssh_dir(alias=alias, path=remote, accept_new_host_keys=accept_new_host_keys)
			if not response.success: return response
			tested = True

	# check base.
	base = Formats.FilePath(path).base(back=1)
	if not os.path.exists(base): 
		os.system(f"mkdir -p {base}")
		if not os.path.exists(base): 
			return r3sponse.error_response(f"Failed to create pull base {base}.")
		if log_level >= 3:
			print(f"Created directory {base}.")

	# fix rsync timestamp bug.
	if empty_directory and directory and not os.path.exists(path):
		os.system(f"mkdir -p {path}")

	# options.
	exclude_str = Files.Array(array=exclude).string(joiner=" --exclude ", sum_first=True)
	include_str = Files.Array(array=include).string(joiner=" --include ", sum_first=True)
	delete_str = Formats.Boolean(delete).convert(true="--delete", false="")
	lremote = serialize_path(gfp.clean(remote), append_last_slash=directory)
	lpath = serialize_path(gfp.clean(path), append_last_slash=directory)
	_command_ = f"rsync -{Formats.Boolean(directory).convert(true='a', false='')}zqt '{alias}:{lremote}' '{lpath}' {exclude_str} {include_str} {delete_str}"
	if log_level >= 3: print(f"Rsync command: [{_command_}].")

	# execute.
	if command: return _command_
	else:
		return execute(
			command=_command_,
			message=f"Successfully pulled [{alias}:{remote}] to [{path}].",
			error=f"Failed to pull [{alias}:{remote}] to [{path}].",
			loader=f"Pulling [{alias}:{remote}] to [{path}]",
		)

	#

# push.
def push(
	# the local path.
	path=None, 
	# the ssht00ls alias.
	alias=None, 
	# the remote path.
	remote=None, 
	# exlude subpaths (list) (leave None to use default).
	exclude=None,
	# include subpaths (list) (leave None to use default).
	include=None,
	# path is directory boolean (leave None to parse automatically).
	directory=True,
	empty_directory=False,
	# update deleted files.
	delete=False,
	# forced mode.
	forced=False,
	# version control.
	safe=False,
	# accept new hosts keys.
	accept_new_host_keys=True,
	# checks.
	checks=True,
	# log level.
	log_level=0,
	# get the command in str.
	command=False,
):
	# checks.
	if exclude == None: exclude = EXCLUDE
	if include == None: include = INCLUDE
	if checks:

		# check alias.
		path = serialize_path(gfp.clean(path))
		remote = serialize_path(gfp.clean(remote))
		#response = aliases.check(alias)
		#if not response.success: return response
		
		# check passphrase.
		#if CONFIG["aliases"][alias]["smart_card"] in [True, "true", "True"]:
		#	response = ENCRYPTION.decrypt(CONFIG["aliases"][alias]["passphrase"])
		#else:
		#	response = ENCRYPTION.decrypt(CONFIG["aliases"][alias]["passphrase"])
		#if not response.success: return response
		#passphrase = response.decrypted.decode()
		
		# tests.
		#response = agent.add(path=CONFIG["aliases"][alias]["private_key"], passphrase=passphrase)
		#if not response["success"]: return response
		response = utils.test_ssht00ls(alias=alias, accept_new_host_keys=accept_new_host_keys)
		if not response.success: return response
		response = utils.test_ssh_path(alias=alias, path=Formats.FilePath(remote).base(), accept_new_host_keys=accept_new_host_keys)
		if not response.success: return response

		# dir.
		if directory == None: directory = os.path.isdir(path)
		elif directory and not os.path.isdir(path):
			return r3sponse.error_response(f"Path {path} is not a directory.")

		"""
		NOTE:
		testing if check remote base can also be included if check==True only.
		"""
		# check remote base.
		base = Formats.FilePath(remote).base(back=1)
		response = utils.test_ssh_dir(alias=alias, path=base, accept_new_host_keys=accept_new_host_keys, create=True, checks=False)
		if not response.success: return response
		if response.created and log_level >= 3: print(f"Created remote directory {base}.")

	# options.
	exclude_str = Files.Array(array=exclude).string(joiner=" --exclude ", sum_first=True)
	include_str = Files.Array(array=include).string(joiner=" --include ", sum_first=True)
	delete_str = Formats.Boolean(delete).convert(true="--delete", false="")
	lremote = serialize_path(gfp.clean(remote), append_last_slash=directory)
	lpath = serialize_path(gfp.clean(path), append_last_slash=directory)
	_command_ = f"rsync -{Formats.Boolean(directory).convert(true='a', false='')}zqt '{lpath}' '{alias}:{lremote}' {exclude_str} {include_str} {delete_str}"
	if log_level >= 3: print(f"Rsync command: [{_command_}].")
	
	# execute.
	if command: return _command_
	else:
		return execute(
			command=_command_,
			message=f"Successfully pushed [{path}] to [{alias}:{remote}].",
			error=f"Failed to push [{path}] to [{alias}:{remote}].",
			loader=f"Pushing [{path}] to [{alias}:{remote}].",
		)

	#

# execute.
def execute( 
	# the command in str.
	command="ls",
	# the success message.
	message="Successfully executed the specified command.",
	# the error message.
	error="Failed to execute the specified command.",
	# loader message.
	loader=None,
):

	# execute.
	if loader != None:
		loader = syst3m.console.Loader(loader, interactive=INTERACTIVE)
	output = syst3m.utils.__execute_script__(command)
	if len(output) > 0 and output[len(output)-1] == "\n": output = output[:-1]

	# handler.
	if "rsync: " in output or "rsync error: " in output or "ssh: " in output:
		if loader != None: loader.stop(success=False)
		print(output)
		return r3sponse.error_response(error)
	else:
		if loader != None: loader.stop()
		return r3sponse.success_response(message)

	#

# main.
if __name__ == "__main__":
	a=1

#
	