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
		if append_last_slash and len(path) > 0 and path[len(path)-1] != "/": path = path+"/"
		else: break
	return path

# get the size of a dir.
def size(path, alias=None, log_level=0):
	if alias == None:
		return r3sponse.success_response(f"Successfully retrieved the size of {path}.", {
			"size":Formats.FilePath(path).size(mode="MB"),
		})
	else:
		return execute(
			command=f"""ssh {DEFAULT_SSH_OPTIONS} {alias} ' python3 /usr/local/lib/ssht00ls/classes/utils/size.py {path} ' '""",
			message=f"Successfully retrieved the size of {alias}:{path}.",
			error=f"Failed to retrieve the size of {alias}:{path}.",
			log_level=log_level,
			serialize=True,)

# index.
def index(path):
	index, dir, ids = Files.Dictionary(path=False, dictionary={}), Files.Directory(path=path), []
	for _path_ in dir.paths(recursive=True, files_only=True, banned=[gfp.clean(f"{path}/Icon\r")], banned_names=[".DS_Store", "__pycache__"]):
		if _path_ not in ids and "/__pycache__/" not in path and "/.DS_Store" not in path: 
			index[_path_] = gfp.mtime(path=_path_, format="seconds")
			ids.append(_path_)
	for _path_ in dir.paths(recursive=True, dirs_only=True, banned=[gfp.clean(f"{path}/Icon\r")], banned_names=[".DS_Store", "__pycache__"]):
		id = _path_+" (d)"
		if os.listdir(_path_) == []: id += " (e)"
		if id not in ids and "/__pycache__/" not in path and "/.DS_Store" not in path: 
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
	log_level=LOG_LEVEL,
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
	_command_ = f"rsync -{Formats.Boolean(directory).convert(true='a', false='')}zqt '{alias}:{lremote}' '{lpath}' {exclude_str} {include_str} {delete_str} --timeout={SSH_TIMEOUT}"
	#_command_ = f"rsync -azqtr '{alias}:{lremote}' '{lpath}' {exclude_str} {include_str} {delete_str}"

	# execute.
	if command: return _command_
	else:
		return execute(
			command=_command_,
			message=f"Successfully pulled [{alias}:{remote}] to [{path}].",
			error=f"Failed to pull [{alias}:{remote}] to [{path}].",
			loader=f"Pulling [{alias}:{remote}] to [{path}]",
			log_level=log_level,
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
	log_level=LOG_LEVEL,
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

	# check remote base.
	# must be excluded from the checks == False.
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
	_command_ = f"rsync -{Formats.Boolean(directory).convert(true='a', false='')}zqt '{lpath}' '{alias}:{lremote}' {exclude_str} {include_str} {delete_str} --timeout={SSH_TIMEOUT}"
	#_command_ = f"rsync -azqtr --rsh=ssh '{lpath}' '{alias}:{lremote}' {exclude_str} {include_str} {delete_str}"
	
	# execute.
	if command: return _command_
	else:
		return execute(
			command=_command_,
			message=f"Successfully pushed [{path}] to [{alias}:{remote}].",
			error=f"Failed to push [{path}] to [{alias}:{remote}].",
			loader=f"Pushing [{path}] to [{alias}:{remote}].",
			log_level=log_level,
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
	# serialize to json (overwrites message & error).
	serialize=False,
	# get the output.
	get_output=False,
	# the log level.
	log_level=0,
):

	# execute.
	if log_level >= 6: print(command)
	if loader != None:
		loader = syst3m.console.Loader(loader, interactive=INTERACTIVE)
	
	# script.

	# version 1.
	#output = syst3m.utils.__execute_script__(command)
	
	# version 2.
	#try:
	#	output = subprocess.check_output(["sh", path]).decode()
	#except subprocess.CalledProcessError as e:
	#	return r3sponse.error_response(f"Failed to execute command [{command}], (output: {e.output}), (error: {e}).")

	# version 3.
	#response = syst3m.console.execute(
	#	command=command,)
	#if not response["success"]: return response
	#output = response.output
	# equal to:
	path = f"/tmp/tmp_script_{Formats.String('').generate()}"
	Files.save(path, command)
	try:
		proc = subprocess.run(
		    ["sh", path],
			check=True,
			capture_output=True,
			text=True,
		)
	except subprocess.CalledProcessError as error:
		error_, output = error.stderr, error.output
		if isinstance(error_, bytes): error_ = error_.decode()
		if isinstance(output, bytes): output = error_.decode()
		return r3sponse.error_response(f"Failed to execute command ({command}), (error: {error_}), (output: {output}).")
	error_, output = proc.stderr, proc.stdout
	if isinstance(error_, bytes): error_ = error_.decode()
	if isinstance(output, bytes): output = error_.decode()
	if error_ != "":
		return r3sponse.error_response(f"Failed to execute command ({command}), (error: {error_}), (output: {output}).")
	if len(output) > 0 and output[len(output)-1] == "\n": output = output[:-1]
	Files.delete(path)

	# handler.
	response = utils.check_errors(output)
	if not response.success:
		if loader != None: loader.stop(success=False)
		return response
		#print(output)
		#return r3sponse.error_response(error)
	else:
		if loader != None: loader.stop()
		if serialize:
			try: response = r3sponse.serialize(Formats.String(output).slice_dict(depth=1))
			except Exception as e: 
				return r3sponse.error_response(f"Failed to serialize output: {output}")
			return response
		else:
			if get_output:
				return r3sponse.success_response(message, {
					"output":output,
				})
			else:
				return r3sponse.success_response(message)

	#
#print(size(path="/tmp/mount", alias="dev.vandenberghinc.com"));quit()

# main.
if __name__ == "__main__":
	a=1

#
	