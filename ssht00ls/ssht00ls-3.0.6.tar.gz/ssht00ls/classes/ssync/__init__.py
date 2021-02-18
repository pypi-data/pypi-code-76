#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from ssht00ls.classes.config import *
from ssht00ls.classes.aliases import aliases
from ssht00ls.classes.agent import agent
import ssht00ls.classes.ssync.utils as ssync_utils 
from ssht00ls.classes.ssync import daemon
from ssht00ls.classes import utils

# the ssync object class.
class SSync(object):
	def __init__(self):
		self.utils = ssync_utils
		if CHECKS and INTERACTIVE:
			response = aliases.sync()
			if not response["success"]: response.crash(traceback=False, json=JSON)
			_ = daemon.sync()
	def mount(self, 
		# the local path.
		path=None, 
		# the remote path.
		remote=None, 
		# ssh alias.
		alias=None,
		# forced.
		forced=False,
		# exclude.
		exclude=['__pycache__', '.DS_Store'],
		# accept new host verification keys.
		accept_new_host_keys=True,
		# log level.
		log_level=0,
	):

		# checks.
		response = r3sponse.check_parameters({
			"path:str":path,
			"remote:str":remote,
			"alias:str":alias,
			"exclude:list":exclude,
			"forced:bool":forced,
			"accept_new_host_keys:bool":accept_new_host_keys, })
		if not response["success"]: return response
		cache_path = gfp.clean(path.split(" (d)")[0], remove_last_slash=True)
		if not forced and os.path.exists(path):
			return r3sponse.error_response(f"Path [{path}] already exists.")
		elif "*mounted*" in str(cache.get(id=cache_path, group="daemons")):
			return r3sponse.error_response(f"Path [{path}] is already mounted.")
		path = gfp.clean(path=path)
		remote = gfp.clean(path=remote)

		# pull.
		response = self.pull(
			path=path, 
			alias=alias, 
			remote=remote, 
			exclude=exclude,
			forced=forced,
			delete=True,
			safe=False,
			log_level=log_level,)
		if not response["success"]: return response

		# start daemon.
		cache.set(id=cache_path, group="daemons", data="*mounted*")
		self.set_mounted_icon(path)
		#status = cache.get(id=cache_path, group="daemons")
		#if status != "*mounted*":
		#	return r3sponse.error_response(f"Failed to set the {path} daemon status.")
		response =  self.daemon(alias=alias, path=path, remote=remote, start=True)
		if not response.success: return response

		# handler.
		return r3sponse.success_response(f"Successfully mounted [{alias}:{remote}] ==> [{path}].")

		#
	def unmount(self, 
		# the local path.
		path=None, 
		# forced required.
		forced=False,
		# sudo required.
		sudo=False,
		# log level.
		log_level=0,
	):

		# checks.
		response = r3sponse.check_parameters({
			"path:str":path,
			"forced:bool":forced,
			"sudo:bool":sudo, })
		if not response["success"]: return response
		path = gfp.clean(path)
		cache_path = gfp.clean(path.split(" (d)")[0], remove_last_slash=True)
		mounted = "*mounted*" in str(cache.get(id=cache_path, group="daemons"))
		if not mounted:
			if not os.path.exists(path):
				return r3sponse.error_response(f"Path [{path}] does not exist.")
			elif not os.path.isdir(path):
				return r3sponse.error_response(f"Path [{path}] is not a directory.")
			status = str(cache.get(id=cache_path, group="daemons"))
			if "*mounted*" not in str(status):
				return r3sponse.error_response(f"Path [{path}] is not mounted (status: {status}).")

		# wait for daemon stop.
		response = self.stop_daemon(path=path)
		if not success: return response

		# handler.
		return r3sponse.success_response(f"Successfully unmounted [{path}].")

		#
	def index(self, path=None, alias=None, log_level=0, checks=True, accept_new_host_keys=True):

		# checks.
		if path == None:
			return r3sponse.error_response(f"Define parameter: path.")
		path = gfp.clean(path)

		# remote.
		if alias != None:

			# checks.
			if checks:
				
				# check alias.
				response = aliases.check(alias)
				if not response["success"]: return response

				# check passphrase.
				if CONFIG["aliases"][alias]["smart_card"] in [True, "true", "True"]:
					response = ENCRYPTION.decrypt(CONFIG["aliases"][alias]["passphrase"])
				else:
					response = ENCRYPTION.decrypt(CONFIG["aliases"][alias]["passphrase"])
				if not response["success"]: return response
				passphrase = response.decrypted.decode()
				
				# tests.
				response = agent.add(path=CONFIG["aliases"][alias]["private_key"], passphrase=passphrase)
				if not response["success"]: return response
				response = utils.test_ssht00ls(alias=alias, accept_new_host_keys=accept_new_host_keys)
				if not response["success"]: return response
				response = utils.test_ssh_path(alias=alias, path=path, accept_new_host_keys=accept_new_host_keys)
				if not response["success"]: return response

			# index.
			return self.utils.execute(
				command=f"""printf 'yes' | ssh {DEFAULT_SSH_OPTIONS} {alias} ' export IPINFO_API_KEY="{IPINFO_API_KEY}" && python3 /usr/local/lib/ssht00ls/classes/ssync/index.py --path {path} --json --non-interactive --no-checks ' """,
				serialize=True,
				log_level=log_level,)

		# local.
		else:
			if checks:
				if not os.path.exists(path):
					return r3sponse.error_response(f"Path [{path}] does not exist.")
				elif not os.path.isdir(path):
					return r3sponse.error_response(f"Path [{path}] is not a directory.")

			# handler.
			dict = self.utils.index(path)
			return r3sponse.success_response(f"Successfully indexed {len(dict)} files from directory [{path}].", {
				"index":dict,
			})

			#
	def set_mounted_icon(self, path):
		if OS in ["osx", "macos"]:
			#os.system(f"cp '{SOURCE_PATH}/static/media/icons/Icon\r' '{path}/Icon\r'")
			icon = f'{SOURCE_PATH}/static/media/icons/mounted.png'
			syst3m.utils.__execute_script__(f"""
				
				#!/bin/bash
				# Set Icon to a File / Folder on macOS

				icon="{icon}"
				dest="{path}"

				# Check inputs

				if [ ! -f $icon ]; then 
					echo "ERROR: File $1 does not exists"
					exit 1
				elif [[ ! $icon =~ .*\.(png|PNG|jpg|JPG) ]]; then
					echo "ERROR: Icon must be a .png|.jpg file"
					exit 1
				elif [ -f $dest ]; then
					folder=false
				elif [ -d $dest ]; then
					folder=true
				else
					echo 'ERROR: File|Folder destination does not exists'
					exit 1
				fi

				# Create icns icon

				sips -i $icon > /dev/null
				DeRez -only icns $icon > /tmp/tmpicns.rsrc

				# Set Icon

				if [ "$folder" = true ]; then
					Rez -append /tmp/tmpicns.rsrc -o $dest$'/Icon\r'
					SetFile -a C $dest
					SetFile -a V $dest$'/Icon\r'
				else
					Rez -append /tmp/tmpicns.rsrc -o $dest
					SetFile -a C $dest
				fi

				# Clean up

				rm /tmp/tmpicns.rsrc
				exit 0

				""")
	# pull & push.
	def pull(self,
		# the local path.
		path=None, 
		# the ssht00ls alias.
		alias=None, 
		# the remote path.
		remote=None, 
		# exlude subpaths (list) (leave None to use default).
		exclude=None,
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
		if checks:
			if CONFIG["aliases"][alias]["smart_card"] in [True, "true", "True"]:
				response = ENCRYPTION.decrypt(CONFIG["aliases"][alias]["passphrase"])
			else:
				response = ENCRYPTION.decrypt(CONFIG["aliases"][alias]["passphrase"])
			if not response["success"]: return response
			passphrase = response.decrypted.decode()
			response = aliases.check(alias)
			if not response["success"]: return response
			response = agent.add(path=CONFIG["aliases"][alias]["private_key"], passphrase=passphrase)
			if not response["success"]: return response
		return self.utils.pull(
			# the local path.
			path=path, 
			# the ssht00ls alias.
			alias=alias, 
			# the remote path.
			remote=remote, 
			# exlude subpaths (list) (leave None to use default).
			exclude=exclude,
			# path is directory boolean (leave None to parse automatically).
			directory=directory,
			empty_directory=empty_directory,
			# update deleted files.
			delete=delete,
			# forced mode.
			forced=forced,
			# version control.
			safe=safe,
			# accept new hosts keys.
			accept_new_host_keys=accept_new_host_keys,
			# checks.
			checks=checks,
			# log level.
			log_level=log_level,
			# get the command in str.
			command=command,)
	def push(self,
		# the local path.
		path=None, 
		# the ssht00ls alias.
		alias=None, 
		# the remote path.
		remote=None, 
		# exlude subpaths (list) (leave None to use default).
		exclude=None,
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
		if checks:
			if CONFIG["aliases"][alias]["smart_card"] in [True, "true", "True"]:
				response = ENCRYPTION.decrypt(CONFIG["aliases"][alias]["passphrase"])
			else:
				response = ENCRYPTION.decrypt(CONFIG["aliases"][alias]["passphrase"])
			if not response["success"]: return response
			passphrase = response.decrypted.decode()
			response = aliases.check(alias)
			if not response["success"]: return response
			response = agent.add(path=CONFIG["aliases"][alias]["private_key"], passphrase=passphrase)
			if not response["success"]: return response
		return self.utils.push(
			# the local path.
			path=path, 
			# the ssht00ls alias.
			alias=alias, 
			# the remote path.
			remote=remote, 
			# exlude subpaths (list) (leave None to use default).
			exclude=exclude,
			# path is directory boolean (leave None to parse automatically).
			directory=directory,
			empty_directory=empty_directory,
			# update deleted files.
			delete=delete,
			# forced mode.
			forced=forced,
			# version control.
			safe=safe,
			# accept new hosts keys.
			accept_new_host_keys=accept_new_host_keys,
			# checks.
			checks=checks,
			# log level.
			log_level=log_level,
			# get the command in str.
			command=command,)
	# initialize a mounted daemon.
	def daemon(self, 
		# the ssh alias.
		alias=None, 
		# the remote path.
		remote=None, 
		# thel local path.
		path=None, 
		# settings.
		start=True,
		# the daemon mode.
		mode="mount",
		# the daemons log level.
		log_level=syst3m.defaults.log_level(default=-1),
		# sandbox (do not delete any files).
		sandbox=False,
		# serialized.
		serialized={},
	):
		if serialized != {}:
			alias, remote, path, start, mode, log_level, sandbox = Files.Dictionary(path=False, dictionary=serialized).unpack({
				"alias":None,
				"remote":None,
				"path":None,
				"start":True,
				"mode":"mount",
				"log_level":syst3m.defaults.log_level(default=-1),
				"sandbox":False,
			})
		if mode in ["synchronize", "sync", "synch"]: mode = "sync"
		if mode not in ["mount", "sync"]:
			return r3sponse.error_response(f"Specified an invalid mode: [{mode}], options: [mount, sync].")
		path = gfp.clean(path)
		remote = gfp.clean(remote)
		_daemon_ = daemon.Daemon({
			"alias":alias,
			"remote":remote,
			"path":path,
			"mode":mode,
			"log_level":log_level,
			"sandbox":sandbox,
			"ssync":self,
			"utils":self.utils,
			"sleeptime":0.25,
		})
		if start: webserver.start_daemon(_daemon_, group="daemons", id=_daemon_.id)
		return r3sponse.success_response("Successfully initialized the daemon", {
			"daemon":_daemon_,
		})
	def stop_daemon(self, path, timeout=60, sleeptime=1):
		return daemon.stop_daemon(path, timeout=timeout, sleeptime=sleeptime)
	
# initialized objects.
ssync = SSync()
