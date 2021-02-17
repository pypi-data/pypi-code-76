#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from ssht00ls.classes.config import *
from ssht00ls.classes.aliases import aliases
from ssht00ls.classes.agent import agent
import ssht00ls.classes.ssync.utils as ssync_utils 
from ssht00ls.classes import utils

# the ssync object class.
class SSync(object):
	def __init__(self):
		aliases.sync()
		self.utils = ssync_utils
		self.sync()
		self.gfp = Formats.FilePath("global")
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
		path = self.gfp.clean(path=path)
		remote = self.gfp.clean(path=remote)

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
		daemon = self.daemon(alias=alias, path=path, remote=remote, start=True)

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
			ip_api_key = os.environ.get("IPINFO_API_KEY")
			output = syst3m.utils.__execute_script__(f"printf 'yes' | ssh {alias} ' export IPINFO_API_KEY="{ip_api_key}" && python3 /usr/local/lib/ssht00ls/classes/ssync/index.py --path {path} --json --non-interactive --no-checks ' ")
			try: response = r3sponse.serialize(output)
			except Exception as e: 
				return r3sponse.error_response(f"Failed to serialize remote {alias} output: {output}")
			return response

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
	# the mounted daemon.
	def sync(self):
		for path in Files.Directory(path=f"{cache.path}/daemons/").paths(recursive=False):
			if not os.path.exists(path.replace("\\","/")): os.remove(path)
	def daemon(self, 
		# the ssh alias.
		alias=None, 
		# the remote path.
		remote=None, 
		# thel local path.
		path=None, 
		# settings.
		start=True,
		# the daemons log level.
		log_level=syst3m.defaults.log_level(default=-1),
		# sandbox (do not delete any files).
		sandbox=False,
		# serialized.
		serialized={},
	):
		if serialized != {}:
			alias, remote, path, start, log_level, sandbox = Files.Dictionary(path=False, dictionary=serialized).unpack({
				"alias":None,
				"remote":None,
				"path":None,
				"start":True,
				"log_level":syst3m.defaults.log_level(default=-1),
				"sandbox":False,
			})
		path = gfp.clean(path)
		remote = gfp.clean(remote)
		daemon = self.Daemon({
			"alias":alias,
			"remote":remote,
			"path":path,
			"log_level":log_level,
			"sandbox":sandbox,
			"ssync":self,
			"sleeptime":0.25,
		})
		if start: webserver.start_daemon(daemon, group="daemons", id=daemon.id)
		return daemon
	def set_mounted_icon(self, path):
		if OS in ["macos", "macos"]:
			#os.system(f"cp '{SOURCE_PATH}/static/media/icons/Icon\r' '{path}/Icon\r'")
			icon = f'{SOURCE_PATH}/static/media/icons/mounted.png'
			syst3m.utils.__execute_script__(f"""
				
				# Take an image and make the image its own icon:
				sips -i {icon}

				# Extract the icon to its own resource file:
				/Developer/Tools/DeRez -only icns {icon} > /tmp/tmpicns.rsrc

				# append this resource to the file you want to icon-ize.
				/Developer/Tools/Rez -append /tmp/tmpicns.rsrc -o {path}

				# Use the resource to set the icon.
				/Developer/Tools/SetFile -a C {path}

				# clean up.
				rm  -fr /tmp/tmpicns.rsrc

				""")
	def stop_daemon(self, path, timeout=60, sleeptime=1):
		cache_path = gfp.clean(path.split(" (d)")[0], remove_last_slash=True)
		cache.set(id=cache_path, data="*stop*", group="daemons")
		stopped = False
		for i in range(int(timeout/sleeptime)):
			status_ = str(cache.get(id=cache_path, group="daemons"))
			if "*stopped*" in status_ or "*crashed*" in status_:
				stopped = True
				break
			time.sleep(sleeptime)
		if stopped:
			return r3sponse.success_response(f"Successfully stopped ssht00ls daemon [{path}].")
		else:
			return r3sponse.error_response(f"Failed to stop ssht00ls daemon [{path}].")
	class Daemon(syst3m.objects.Thread):
		def __init__(self, attributes={}):
			self.utils = ssync_utils
			syst3m.objects.Thread.__init__(self)
			self.assign(attributes)
			self.path = gfp.clean(self.path)
			self.id = f"{self.alias}:{self.remote} {self.path}"
			try:self.log_level
			except: self.log_level = -1
			self.last_index = {}
			self.last_remote_index = {}
			self.cache_path = gfp.clean(self.path.split(" (d)")[0], remove_last_slash=True)
		def run(self):

			# logs.
			if self.log_level >= 0: 
				loader = syst3m.console.Loader(f"Checking daemon {self.id}", interactive=INTERACTIVE)

			# checks.
			status = str(cache.get(id=self.cache_path, group="daemons"))
			if "*mounted*" not in status:
				if self.log_level >= 0: loader.stop(success=False)
				self.crash(f"ssht00ls daemon ({self.id}): Path [{self.path}] is not mounted (status: {status}).")
			if self.log_level >= 0: 
				loader.mark(f"Checking mountpoint {self.path}")
			if not os.path.exists(self.path):
				if self.log_level >= 0: loader.stop(success=False)
				self.crash(f"ssht00ls daemon ({self.id}): Path [{self.path}] does not exist.")
			if not os.path.isdir(self.path):
				if self.log_level >= 0: loader.stop(success=False)
				self.crash(f"ssht00ls daemon ({self.id}): Path [{self.path}] is not a directory.")


			# check alias.
			if self.log_level >= 0: 
				loader.mark(f"Checking alias {self.alias}")
			response = aliases.check(self.alias)
			if not response["success"]: 
				if self.log_level >= 0: loader.stop(success=False)
				self.crash(response=response)

			# get index.
			if self.log_level >= 0: 
				loader.mark(f"Indexing [{self.path}] & [{self.alias}:{self.remote}].")
			response = self.index(short=True)
			if not response["success"]: 
				if self.log_level >= 0: loader.stop(success=False)
				self.crash(response=response)

			# start success.
			if self.log_level >= 0: 
				loader.mark(f"Starting daemon {self.id}")
				loader.stop()

			# start.
			while True:

				# check stop command.
				status = str(cache.get(id=self.cache_path, group="daemons"))
				if "*stop*" in status or "*unmounting*" in status:
					break

				# if file no longer exists stop daemon.
				if not os.path.exists(self.path): 
					self.crash(f"ssht00ls daemon ({self.id}): Mounted directory [{self.path}] from [{self.alias}:{self.remote}] no longer exists.")

				# sync.
				response = self.sync()
				if self.log_level >= 1:
					r3sponse.log(response=response)
				if not response["success"]: 
					self.crash(f"ssht00ls daemon ({self.id}) error: {response.error}", unmount=False)

				# sleep.
				time.sleep(self.sleeptime)

			# stop.
			self.stop()

			#
		def stop():
			response = self.unmount()
			if not response["success"]: self.crash(f"ssht00ls daemon ({self.id}) error: {response['error']}")
			cache.set(id=self.cache_path, data="*stopped*", group="daemons")
			if self.log_level >= 0: print(f"Stopped daemon {self.id}")
		def crash(self, error=None, response=None, unmount=True):
			if response != None: error = response["error"]
			if unmount:
				response = self.unmount()
				if not response["success"]: 
					cache.set(id=self.cache_path, data="*crashed*", group="daemons")
					raise ValueError(f"ssht00ls daemon ({self.id}) error: {response['error']}")
			cache.set(id=self.cache_path, data="*crashed*", group="daemons")
			raise ValueError(error)
		def unmount(self):
			if os.path.exists(self.path):
				response = self.sync()
				if not response["success"]: return response
				cache.set(id=self.cache_path, data="*unmounting*", group="daemons")
				time.sleep(1)
				response = self.delete(self.path, remote=False, subpath=False,)
				if not response["success"]: return response
			return r3sponse.success_response("Successfully unmounted.")
		def index(self, short=False):

			# index.
			remote_response = ssync.index(path=self.path, alias=self.alias, checks=False)
			if not remote_response["success"]:  return remote_response
			response = ssync.index(path=self.path)
			if not response["success"]:  return response
			index, remote_index, clean_index, remote_clean_index, all_paths = response["index"], remote_response["index"], {}, {}, []
			for path in list(index.keys()):
				subpath = self.subpath(path)
				if subpath not in all_paths: 
					all_paths.append(subpath)
				subpath = subpath.split(" (d)")[0] # unpack after appended to all_paths.
				clean_index[subpath] = index[path]
			for path in list(remote_index.keys()):
				subpath = self.subpath(path)
				if subpath not in all_paths: 
					all_paths.append(subpath)
				subpath = subpath.split(" (d)")[0] # unpack after appended to all_paths.
				remote_clean_index[subpath] = remote_index[path]
			synchronized, mismatches = self.synchronized(clean_index, remote_clean_index, all_paths)
			if short in ["automatic", "auto"]:
				if not synchronized: short = False
			if short:
				if self.last_index == {}:
					self.last_index["0"] = clean_index
				if self.last_remote_index == {}:
					self.last_remote_index["0"] = remote_clean_index
				return r3sponse.success_response(f"Successfully indexed [{self.alias}:{self.path}] & [{self.path}].", {
					"synchronized":synchronized,
					"index":index,
					"remote_index":remote_index,
				})
			else: return self.process_index(clean_index, remote_clean_index, mismatches)
			#
		def process_index(self, index, remote_index, mismatches):

			# iterate.
			updates, deletions = {}, {}
			for subpath, info in mismatches.items():

				# vars.
				directory = info["directory"]
				empty_directory = info["empty_directory"]
				subpath = subpath.split(" (d)")[0] # just to be sure.
				lfullpath, rfullpath = self.fullpath(subpath), self.fullpath(subpath, remote=True)
				try: lmtime = index[subpath]
				except KeyError: lmtime = None
				try: rmtime = remote_index[subpath]
				except KeyError: rmtime = None
				last_lmtime = self.get_last_index(subpath)
				last_rmtime = self.get_last_index(subpath, remote=True)

				# wanted vars.
				local_to_remote, remote_to_local = False, False
				options = []
				
				# should not happen.
				if rmtime == None and lmtime == None: 
					self.set_last_index(index) ; self.set_last_index(remote_index, remote=True)
					return r3sponse.error_response(f"No remote & local modification time present. (path: {subpath}), (rmtime: {rmtime}), (lmtime: {lmtime}), (last_rmtime: {last_rmtime}), (last_lmtime: {last_lmtime}), index: {json.dumps(index,indent=4)}, remote index: {json.dumps(remote_index,indent=4)}.")

				# one missing.
				elif rmtime == None or lmtime == None:
					
					# remote deleted a file.
					if rmtime == None and lmtime != None and (last_lmtime != None or last_rmtime != None):
						if self.log_level >= 3:
							print(f"Remote deleted a file (path: {subpath}) (rmtime: {rmtime}), (lmtime: {lmtime}), (last_lmtime: {last_lmtime}).")
						remote_to_local = True
						options.append("delete")

					# local deleted a file.
					elif rmtime != None and lmtime == None and last_lmtime != None:
						if self.log_level >= 3:
							print(f"Local deleted a file (path: {subpath}) (rmtime: {rmtime}), (lmtime: {lmtime}), (last_lmtime: {last_lmtime}).")
						local_to_remote = True
						options.append("delete")

					# local created a file.
					elif rmtime == None and lmtime != None and last_lmtime == None:
						if self.log_level >= 3:
							print(f"Local created a file (path: {subpath}) (rmtime: {rmtime}), (lmtime: {lmtime}), (last_lmtime: {last_lmtime}).")
						local_to_remote = True

					# remote created a file.
					elif rmtime != None and lmtime == None and last_lmtime == None:
						if self.log_level >= 3:
							print(f"Remote created a file (path: {subpath}) (rmtime: {rmtime}), (lmtime: {lmtime}), (last_lmtime: {last_lmtime}).")
						remote_to_local = True

					# should not happen.
					else:
						self.set_last_index(index) ; self.set_last_index(remote_index, remote=True)
						return r3sponse.error_response(f"Should not happen (#3243443). (path: {subpath}), (rmtime: {rmtime}), (lmtime: {lmtime}), (last_rmtime: {last_rmtime}), (last_lmtime: {last_lmtime}), index: {json.dumps(index,indent=4)}, remote index: {json.dumps(remote_index,indent=4)}.")

				# both present.
				elif rmtime != None and lmtime != None:

					# same mtime.
					if str(rmtime) == str(lmtime):
						a=1
					
					# # synchronize remote to local.
					elif rmtime > lmtime:
						remote_to_local = True

					# # synchronize local to remote.
					elif rmtime < lmtime:
						local_to_remote = True

					# should not happen.
					else:
						self.set_last_index(index) ; self.set_last_index(remote_index, remote=True)
						return r3sponse.error_response(f"Unable to compare rmtime: {rmtime} & lmtime: {lmtime}. (path: {subpath}), (rmtime: {rmtime}), (lmtime: {lmtime}), (last_rmtime: {last_rmtime}), (last_lmtime: {last_lmtime}), index: {json.dumps(index,indent=4)}, remote index: {json.dumps(remote_index,indent=4)}.")

				# exceptions.
				else:
					self.set_last_index(index) ; self.set_last_index(remote_index, remote=True)
					return r3sponse.error_response(f"Should not happen (#407294). (path: {subpath}), (rmtime: {rmtime}), (lmtime: {lmtime}), (last_rmtime: {last_rmtime}), (last_lmtime: {last_lmtime}), index: {json.dumps(index,indent=4)}, remote index: {json.dumps(remote_index,indent=4)}.")

				# do not remove this exception.
				# it is required for safe edits, to make sure a dir never gets synced unless it is created / removed.
				# also required by the multiprocessing idexing.
				if directory and local_to_remote != None and remote_to_local != None and "delete" not in options and not empty_directory:
					pass
				else:

					# add to updates.
					if local_to_remote and remote_to_local:
						self.set_last_index(index) ; self.set_last_index(remote_index, remote=True)
						return r3sponse.error_response(f"Can not synchronize both remote to local & local to remote (rmtime: {rmtime}) (lmtime: {lmtime}), (last_rmtime: {last_rmtime}) (last_lmtime: {last_lmtime}), index: {json.dumps(index,indent=4)}, remote index: {json.dumps(remote_index,indent=4)}.")
					if "delete" in options: 
						if self.log_level >= 1: 
							if local_to_remote:
								print(f"Deletion required {lfullpath} {self.alias}:{rfullpath} (rmtime: {rmtime}) (lmtime: {lmtime}), (last_rmtime: {last_rmtime}) (last_lmtime: {last_lmtime})")
							else:
								print(f"Deletion required {self.alias}:{rfullpath} {lfullpath} (rmtime: {rmtime}) (lmtime: {lmtime}), (last_rmtime: {last_rmtime}) (last_lmtime: {last_lmtime})")
						deletions[subpath] = {
							"options":options,
							"remote_to_local":remote_to_local,
							"local_to_remote":local_to_remote,
							"directory":directory,
							"empty_directory":empty_directory,}
					elif remote_to_local or local_to_remote:
						if self.log_level >= 1: 
							if local_to_remote:
								print(f"Update required {lfullpath} {self.alias}:{rfullpath} (rmtime: {rmtime}) (lmtime: {lmtime}), (last_rmtime: {last_rmtime}) (last_lmtime: {last_lmtime})")
							else:
								print(f"Update required {self.alias}:{rfullpath} {lfullpath} (rmtime: {rmtime}) (lmtime: {lmtime}), (last_rmtime: {last_rmtime}) (last_lmtime: {last_lmtime})")
						updates[subpath] = {
							"options":options,
							"remote_to_local":remote_to_local,
							"local_to_remote":local_to_remote,
							"directory":directory,
							"empty_directory":empty_directory,}
			# handler.
			self.set_last_index(index) ; self.set_last_index(remote_index, remote=True)
			return r3sponse.success_response(f"Successfully indexed [{self.alias}:{rfullpath}] & [{lfullpath}].", {
				"synchronized":len(updates) == 0 and len(deletions) == 0,
				"updates":updates,
				"deletions":deletions,
				"index":index,
				"remote_index":remote_index,
			})
		def local_to_remote(self, path, info, directory=False, empty_directory=False, forced=False, delete=False, command=False):
			lfullpath, rfullpath = self.fullpath(path, append_slash=directory), self.fullpath(path, remote=True, append_slash=directory)
			if self.log_level >= 0: print(f"Synchronizing {lfullpath} to {self.alias}:{rfullpath} (directory: {directory}) (delete: {delete}) (forced: {forced}).")
			return self.ssync.push(
				path=lfullpath, 
				alias=self.alias, 
				remote=rfullpath, 
				directory=directory,
				empty_directory=empty_directory,
				delete=delete,
				forced=forced,
				safe=False,
				accept_new_host_keys=True,
				checks=False,
				command=command,
				log_level=self.log_level,)
		def remote_to_local(self, path, info, directory=False, empty_directory=False, forced=False, delete=False, command=False):
			lfullpath, rfullpath = self.fullpath(path, append_slash=directory), self.fullpath(path, remote=True, append_slash=directory)
			if self.log_level >= 0: print(f"Synchronizing {self.alias}:{rfullpath} to {lfullpath} (directory: {directory}) (delete: {delete}) (forced: {forced}).")
			return self.ssync.pull(
				path=lfullpath, 
				alias=self.alias, 
				remote=rfullpath, 
				directory=directory,
				empty_directory=empty_directory,
				delete=delete,
				forced=forced,
				safe=False,
				accept_new_host_keys=True,
				checks=False,
				command=command,
				log_level=self.log_level,)
		def synchronized(self, clean_index, remote_clean_index, all_paths):
			mismatches = {}
			for fullpath in all_paths:
				subpath = fullpath.split(" (d)")[0]
				lmtime, rmtime, synchronized = None, None, True
				try: 
					lmtime = clean_index[subpath]
				except KeyError: a=1
				try:
					rmtime = remote_clean_index[subpath]
				except KeyError: a=1
				if lmtime != None or rmtime != None:
					synchronized = lmtime == rmtime
				# skip dirs with not the same mtime but that do both have a mtime.
				if " (d)" in fullpath and lmtime != None and rmtime != None and lmtime != rmtime:
					if self.log_level >= 3:
						print(f"Revert directory {subpath} from synchronized {synchronized} to True")
					synchronized = True
				if not synchronized: 
					mismatches[subpath] = {
						"path":subpath,
						"directory":" (d)" in fullpath,
						"empty_directory":" (d)" in fullpath and " (e)" in fullpath,
						"local_mtime":lmtime,
						"remote_mtime":rmtime,
					}
			synchronized = len(mismatches) == 0
			if self.log_level >= 3: print(f'synchronized: {synchronized} clean_index: {json.dumps(clean_index,indent=4)}, remote_clean_index: {json.dumps(remote_clean_index,indent=4)} mismatches: {json.dumps(mismatches, indent=4)}.')
			return synchronized, mismatches
		def subpath(self, fullpath, remote=False, append_slash=False):
			if remote: path = self.remote
			else: path = self.path
			s = ""
			if append_slash: s = "/"
			return fullpath.replace(path+s, "").replace("//","/").replace("//","/").replace("//","/").replace("//","/").replace("//","/").replace("//","/").replace("//","/").replace("//","/").replace("//","/").replace("//","/")
		def fullpath(self, subpath, remote=False, append_slash=False):
			if remote: path = self.remote
			else: path = self.path
			s = ""
			if append_slash: s = "/"
			return f"{path}/{subpath}{s}".replace("//","/").replace("//","/").replace("//","/").replace("//","/").replace("//","/").replace("//","/").replace("//","/").replace("//","/").replace("//","/").replace("//","/").replace("//","/").replace("//","/").replace("//","/").replace("//","/").replace("//","/")
		def delete(self, path, remote=False, subpath=True):

			# sandbox.
			path = self.utils.serialize_path(gfp.clean(path))
			if subpath: path = self.fullpath(path, remote=remote)
			if self.sandbox: 
				if remote:
					msg = f"Sandbox enabled, skip deletion of {self.alias}:{path}."
					if self.log_level >= 0: print(msg)
					return r3sponse.success_response(msg)
				else:
					msg = f"Sandbox enabled, skip deletion of {path}."
					if self.log_level >= 0: print(msg)
					return r3sponse.success_response(msg)

			# logs.
			if self.log_level >= 0:
				if remote: print(f"Deleting {self.alias}:{path}.")
				else:print(f"Deleting {path}.")
			
			# local to remote.
			if remote:
				os.system(f"""ssh {self.alias} " printf 'y' | rm -fr '{path}' " """)
				response = utils.test_ssh_path(alias=self.alias, path=path)
				if response.error != None and f"{path} does not exist" not in response.error:
					return r3sponse.error_response(f"Failed to delete {path}, error: {response.error}")
				return r3sponse.success_response(f"Successfully deleted {self.alias}:{path}")

			# remote to local.
			else:
				os.system(f"printf 'y' | rm -fr '{path}' ")
				if os.path.exists(path):
					return r3sponse.error_response(f"Failed to delete {path}")
				return r3sponse.success_response(f"Successfully deleted {path}")
		def sync(self, multiprocessing=True, max_batch_size=50):

			# get index.
			response = self.index(short="auto")
			if not response["success"]:  return response
			elif response.synchronized:
				if self.log_level > 0:
					print(f"Directories [{self.alias}:{self.path}] & [{self.path}] are already synchronized.")
				if self.log_level >= 3:
					return r3sponse.success_response(f"Directories [{self.alias}:{self.path}] & [{self.path}] are already synchronized, index: {json.dumps(response.index, indent=4)}, remote index: {json.dumps(response.remote_index, indent=4)}.")
				else:
					return r3sponse.success_response(f"Directories [{self.alias}:{self.path}] & [{self.path}] are already synchronized.")
			updates,deletions = response.unpack(["updates", "deletions"])
			if multiprocessing and len(updates) < max_batch_size:
				multiprocessing = False

			# parallel multiprocessing.
			if False and multiprocessing:
			
				# order updates by dir depth from deepest to min.
				# create depth index.
				dir_updates, depths, max_depth = {}, {}, 0
				for path, info in updates.items():
					if info["directory"]: dir_updates[path] = info
					else:
						depth = len(gfp.clean(path, remove_double_slash=True, remove_first_slash=True, remove_last_slash=True).split("/"))
						if depth >= max_depth: max_depth = depth
						try: depths[str(depth)]
						except KeyError: depths[str(depth)] = {}
						depths[str(depth)][path] = info
				
				# add batches from highest depth to lowest.
				update_batches, batch_size, inside_batch_size, last_depth = {}, 0, 0, None
				for i in range(max_depth+1):
					depth, found = max_depth-i, True
					try: depths[str(depth)]
					except KeyError: found = False
					if found:
						if (last_depth != None and last_depth != depth) or (inside_batch_size >= max_batch_size): 
							last_depth = depth
							batch_size += 1
							inside_batch_size = 0
						for path, info in depths[str(depth)].items():
							if inside_batch_size >= max_batch_size: 
								last_depth = depth
								batch_size += 1
								inside_batch_size = 0
							try: update_batches[str(batch_size)]
							except KeyError: update_batches[str(batch_size)] = {}
							update_batches[str(batch_size)][path] = info
							inside_batch_size += 1
				# add directories.
				for path, info in dir_updates.items():
					if inside_batch_size >= max_batch_size: 
						batch_size += 1
						inside_batch_size = 0
					try: update_batches[str(batch_size)]
					except KeyError: update_batches[str(batch_size)] = {}
					update_batches[str(batch_size)][path] = info
					inside_batch_size += 1

				# iterate updates.
				commands = {}
				for batch_size, batch in update_batches.items():
					commands[batch_size] = []
					for path, info in batch.items():
						if self.log_level >= 0: print(f"Updating {path}.")

						# local to remote.
						if info["local_to_remote"]:
							if info["directory"] in [True, "True", "TRUE", "true"]: 
								commands[batch_size] += [self.local_to_remote(path, info, directory=True, command=True)]
							else: 
								commands[batch_size] += [self.local_to_remote(path, info, command=True)]

						# remote to local.
						elif info["remote_to_local"]:
							if info["directory"] in [True, "True", "TRUE", "true"]: 
								commands[batch_size] += [self.remote_to_local(path, info, directory=True, command=True)]
							else: 
								commands[batch_size] += [self.remote_to_local(path, info, command=True)]

				# execute commands.
				for batch_size, batch in commands.items():
					loader, c = None, len(batch)
					if self.log_level >= 0: loader = f"Synchronizing {c} file(s)."
					msg = f"Successfully synchronized {c} file(s)."
					error = f"Failed to synchronize {c} file(s)."
					command = Files.Array(array=batch).string(joiner=" & ")
					response = self.utils.execute(command=command, error=error, message=msg, loader=loader)
					if not response.success:
						response = self.utils.execute(command=command, error=error, message=msg, loader=loader)
						if not response.success:
							return response

			# no multiprocessing.
			else:

				# sum together as one command
				command = False

				# iterate updates.
				dirs, commands, c = {}, [], 0
				for path, info in updates.items():
					if self.log_level >= 0: print(f"Updating {path}.")

					# local to remote.
					if info["local_to_remote"]:
						if info["directory"] in [True, "True", "TRUE", "true"]: dirs[path] = info
						else: 
							commands += [self.local_to_remote(path, info, command=command)]
							c += 1

					# remote to local.
					elif info["remote_to_local"]:
						if info["directory"] in [True, "True", "TRUE", "true"]: dirs[path] = info
						else: 
							commands += [self.remote_to_local(path, info, command=command)]
							c += 1

				# iterate excepted dirs.
				for path, info in dirs.items():

					# local to remote.
					if info["local_to_remote"]:
						commands += [self.local_to_remote(path, info, directory=True, command=command)]
						c += 1

					# remote to local.
					elif info["remote_to_local"]:
						commands += [self.remote_to_local(path, info, directory=True, command=command)]
						c += 1

				# execute commands.
				if command:
					loader = None
					if self.log_level >= 0: loader = f"Synchronizing {c} file(s)."
					msg = f"Successfully synchronized {c} file(s)."
					error = f"Failed to synchronize {c} file(s)."
					command = Files.Array(array=commands).string(joiner=" && ")
					response = self.utils.execute(command=command, error=error, message=msg, loader=loader)
					if not response.success:
						response = self.utils.execute(command=command, error=error, message=msg, loader=loader)
						if not response.success:
							return response

			# push deletions.
			for path, info in deletions.items():
				if info["remote_to_local"]:
					response = self.delete(path, remote=False)
				else:
					response = self.delete(path, remote=True)
				if not response["success"]: return response
				self.reset_last_index(path, remote="both")

			# check synchronized index.
			response = self.index(short=True)
			if not response["success"]: return response
			elif not response.synchronized:
				if self.log_level <= -1:
					return r3sponse.error_response(f"Failed to synchronize [{self.alias}:{self.remote}] & [{self.path}].")		
				else:
					index, remote_index = response.index, response.remote_index
					mismatches, likeys, rikeys = {}, list(index.keys()), list(remote_index.keys())
					for i in likeys:
						if i not in rikeys:
							try: lmtime = index[i]
							except: lmtime = None
							try: rmtime = remote_index[i]
							except: rmtime = None
							if lmtime != rmtime:
								mismatches[i] = {
									"path":i,
									"local_mtime":lmtime,
									"remote_mtime":rmtime,
								}
					for i in rikeys:
						if i not in likeys:
							try: lmtime = index[i]
							except: lmtime = None
							try: rmtime = remote_index[i]
							except: rmtime = None
							if lmtime != rmtime:
								mismatches[i] = {
									"path":i,
									"local_mtime":lmtime,
									"remote_mtime":rmtime,
								}
					return r3sponse.error_response(f"Failed to synchronize [{self.alias}:{self.remote}] & [{self.path}], mismatches: {json.dumps(mismatches, indent=4)}].")

			# handler.
			return r3sponse.success_response(f"Successfully synchronized [{self.alias}:{self.path}] & [{self.path}].")
		def set_last_index(self, index, remote=False, depth=25):
			if not remote: indexes = self.last_index
			else: indexes = self.last_remote_index
			count = len(indexes)
			if count > depth:
				new = {}
				for key,value in indexes.items():
					key = int(key)
					if key > 0:
						new[str(key-1)] = value
				new[str(depth)] = index
				if not remote: self.last_index = new
				else: self.last_remote_index = new
			else:
				indexes[str(len(indexes))] = index
				if not remote: self.last_lmtime = indexes
				else: self.last_rmtime = indexes
		def reset_last_index(self, id, remote=False):
			if remote == "both":
				self.reset_last_index(id, remote=False)
				self.reset_last_index(id, remote=True)
			else:
				if not remote: indexes = self.last_index
				else: indexes = self.last_remote_index
				for depth in list(indexes.keys()):
					try: 
						index = indexes[depth]
						index[id]
						indexes[depth][id] = None
					except KeyError: a=1
				if not remote: self.last_index = indexes
				else: self.last_remote_index = indexes
		def get_last_index(self, id, remote=False):
			if not remote: indexes = self.last_index
			else: indexes = self.last_remote_index
			value = None
			for _, index in indexes.items():
				try: value = index[id]
				except KeyError: a=1
				if value not in ["None", None, "none"]:
					break
			if self.log_level >= 6:
				print(f"Last index ({id}) {value}) (remote: {remote}), indexes: {indexes}.")
			return value
# initialized objects.
ssync = SSync()

#daemon = ssync.daemon(path="/tmp/testmount.small", remote="/tmp/testmount.small", alias="dev.vandenberghinc.com", start=False)
#response = daemon.index(short=True)
#print(response)
#quit()

#print(ssync.mount(
#	alias="dev.vandenberghinc.com",
#	remote="/tmp/testmount",
#	path="/tmp/testmount",))
#quit()