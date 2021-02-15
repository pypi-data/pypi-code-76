#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from ssht00ls.classes.config import *
from ssht00ls.classes import utils
from ssht00ls.classes.aliases import aliases
from ssht00ls.classes.agent import agent

# the ssync object class.
class SSync(object):
	def __init__(self):
		self.exclude = ['__pycache__', '.DS_Store']
		aliases.sync()
		self.sync()
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
		if not response.success: return response
		elif not forced and os.path.exists(path):
			return r3sponse.error_response(f"Path [{path}] already exists.")
		elif "*mounted*" in str(cache.get(id=path, group="daemons")):
			return r3sponse.error_response(f"Path [{path}] is already mounted.")
		path = utils.clean_path(path)
		remote = utils.clean_path(remote)

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
		if not response.success: return response

		# start daemon.
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
		if not response.success: return response
		path = utils.clean_path(path)
		mounted = "*mounted*" in str(cache.get(id=path, group="daemons"))
		if not mounted:
			if not os.path.exists(path):
				return r3sponse.error_response(f"Path [{path}] does not exist.")
			elif not os.path.isdir(path):
				return r3sponse.error_response(f"Path [{path}] is not a directory.")
			elif "*mounted*" not in str(cache.get(id=path, group="daemons")):
				return r3sponse.error_response(f"Path [{path}] is not mounted.")

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
		path = utils.clean_path(path)

		# remote.
		if alias != None:

			# checks.
			if checks:
				
				# check alias.
				response = aliases.check(alias)
				if not response.success: return response

				# check passphrase.
				if CONFIG["aliases"][alias]["smart_card"] in [True, "true", "True"]:
					response = ENCRYPTION.decrypt(CONFIG["aliases"][alias]["passphrase"])
				else:
					response = ENCRYPTION.decrypt(CONFIG["aliases"][alias]["passphrase"])
				if not response.success: return response
				passphrase = response.decrypted.decode()
				
				# tests.
				response = agent.add(path=CONFIG["aliases"][alias]["private_key"], passphrase=passphrase)
				if not response["success"]: return response
				response = utils.test_ssht00ls(alias=alias, accept_new_host_keys=accept_new_host_keys)
				if not response.success: return response
				response = utils.test_ssh_path(alias=alias, path=path, accept_new_host_keys=accept_new_host_keys)
				if not response.success: return response

			# index.
			output = syst3m.utils.__execute_script__(f"printf 'yes' | ssh {alias} ' python3 /usr/local/lib/ssht00ls/classes/ssync/index.py --path {path} --json ' ")
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

			# index.
			index = Files.Dictionary(path=False, dictionary={})
			for _path_ in Files.Directory(path=path).paths(recursive=True):
				fp = Formats.FilePath(_path_)
				name = fp.name()
				if name not in [".DS_Store", "__pycache__"]:
				id = _path_
				if fp.directory(): id += " (d)"
				basepath = fp.base()
				base = Formats.FilePath(basepath)
				if base.name() not in ["__pycache__"]:
					known = base.exists()
					if known and basepath not in path:
						try: index.dictionary[basepath+" (d)"]
						except: known = False
					if known:
						index[base.path+" (d)"] = base.mtime(format="seconds")
					index[id] = fp.mtime(format="seconds")
			index.dictionary = index.sort(alphabetical=True)

			# handler.
			return r3sponse.success_response(f"Successfully indexed {len(index.dictionary)} files from directory [{path}].", {
				"index":index.dictionary,
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
		directory=None,
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
	):	
		# checks.
		if checks:

			# check alias.
			path = utils.clean_path(path)
			remote = utils.clean_path(remote)
			response = aliases.check(alias)
			if not response.success: return response
			
			# check passphrase.
			if CONFIG["aliases"][alias]["smart_card"] in [True, "true", "True"]:
				response = ENCRYPTION.decrypt(CONFIG["aliases"][alias]["passphrase"])
			else:
				response = ENCRYPTION.decrypt(CONFIG["aliases"][alias]["passphrase"])
			if not response.success: return response
			passphrase = response.decrypted.decode()
			
			# tests.
			response = agent.add(path=CONFIG["aliases"][alias]["private_key"], passphrase=passphrase)
			if not response["success"]: return response
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
		elif directory and checks:
			response = utils.test_ssh_dir(alias=alias, path=remote, accept_new_host_keys=accept_new_host_keys)
			if not response.success: return response
			tested = True

		# check base.
		base = Formats.FilePath(path).base(back=1)
		if not os.path.exists(base): os.system(f"mkdir -p {base}")

		# pull.
		if exclude == None: exclude = self.exclude
		exclude_str = ""
		for i in exclude: exclude_str += f"--exclude {i} "
		delete_str = Formats.Boolean(delete).convert(true="--delete", false="")
		command = f"rsync -{Formats.Boolean(directory).convert(true='a', false='')}zqt {alias}:{remote} {path} {exclude_str}{delete_str}"
		loader = syst3m.console.Loader(f"Pulling [{alias}:{remote}] to [{path}]")
		output = syst3m.utils.__execute_script__(command)
		if len(output) > 0 and output[len(output)-1] == "\n": output = output[:-1]
		cache.set(id=path, data="*mounted*", group="daemons")
		
		# handler.
		if "rsync: " in output or "rsync error: " in output:
			loader.stop(success=False)
			print(output)
			return r3sponse.error_response(f"Failed to pull [{alias}:{remote}] to [{path}].")
		else:
			loader.stop()
			return r3sponse.success_response(f"Successfully pulled [{alias}:{remote}] to [{path}].")

		#
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
		directory=None,
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
	):
		# checks.
		if checks:

			# check alias.
			path = utils.clean_path(path)
			remote = utils.clean_path(remote)
			response = aliases.check(alias)
			if not response.success: return response
			
			# check passphrase.
			if CONFIG["aliases"][alias]["smart_card"] in [True, "true", "True"]:
				response = ENCRYPTION.decrypt(CONFIG["aliases"][alias]["passphrase"])
			else:
				response = ENCRYPTION.decrypt(CONFIG["aliases"][alias]["passphrase"])
			if not response.success: return response
			passphrase = response.decrypted.decode()
			
			# tests.
			response = agent.add(path=CONFIG["aliases"][alias]["private_key"], passphrase=passphrase)
			if not response["success"]: return response
			response = utils.test_ssht00ls(alias=alias, accept_new_host_keys=accept_new_host_keys)
			if not response.success: return response
			response = utils.test_ssh_path(alias=alias, path=Formats.FilePath(remote).base(), accept_new_host_keys=accept_new_host_keys)
			if not response.success: return response

		# dir.
		if directory == None: directory = os.path.isdir(path)
		elif directory and not os.path.isdir(path):
			return r3sponse.error_response(f"Path {path} is not a directory.")

		# check remote base.
		base = Formats.FilePath(remote).base(back=1)
		response = utils.test_ssh_dir(alias=alias, path=base, accept_new_host_keys=accept_new_host_keys, create=True, checks=False)
		if not response.success: return response

		# push.
		if exclude == None: exclude = self.exclude
		exclude_str = ""
		for i in exclude: exclude_str += f"--exclude {i} "
		delete_str = Formats.Boolean(delete).convert(true="--delete", false="")
		command = f"rsync -{Formats.Boolean(directory).convert(true='a', false='')}zqt {path} {alias}:{remote} {exclude_str}{delete_str}"
		loader = syst3m.console.Loader(f"Pushing [{path}] to [{alias}:{remote}].")
		output = syst3m.utils.__execute_script__(command)
		if len(output) > 0 and output[len(output)-1] == "\n": output = output[:-1]
		cache.set(id=path, data="*mounted*", group="daemons")
		
		# handler.
		if "rsync: " in output or "rsync error: " in output:
			loader.stop(success=False)
			print(output)
			return r3sponse.error_response(f"Failed to push [{path}] to [{alias}:{remote}].")
		else:
			loader.stop()
			return r3sponse.success_response(f"Successfully pushed [{path}] to [{alias}:{remote}].")


		#
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
		log_level=1,
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
				"log_level":-1,
				"sandbox":False,
			})
		path = utils.clean_path(path)
		remote = utils.clean_path(remote)
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
	def stop_daemon(self, path, timeout=60, sleeptime=1):
		cache.set(id=path, data="*stop*", group="daemons")
		stopped = False
		for i in range(int(timeout/sleeptime)):
			status_ = cache.get(id=path, group="daemons")
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
			syst3m.objects.Thread.__init__(self)
			self.assign(attributes)
			self.path = utils.clean_path(self.path)
			self.id = f"{self.alias}:{self.remote} {self.path}"
			try:self.log_level
			except: self.log_level = -1
			self.last_index = {}
			self.last_remote_index = {}
		def run(self):

			# logs.
			if self.log_level >= 0: print(f"Starting daemon {self.id}")

			# checks.
			if "*mounted*" not in str(cache.get(id=self.path, group="daemons")):
				self.crash(f"ssht00ls daemon ({self.id}): Path [{self.path}] is not mounted.")
			elif not os.path.exists(self.path):
				self.crash(f"ssht00ls daemon ({self.id}): Path [{self.path}] does not exist.")
			elif not os.path.isdir(self.path):
				self.crash(f"ssht00ls daemon ({self.id}): Path [{self.path}] is not a directory.")

			# check alias.
			response = aliases.check(self.alias)
			if not response.success: self.crash(response.error)

			# get index.
			response = self.index(short=True)
			if not response.success: self.crash(response.error)
			self.last_index = response.index
			self.last_remote_index = response.remote_index

			# start.
			while True:

				# check stop command.
				status = cache.get(id=self.path, group="daemons")
				if "*stop*" in status or "*unmounting*" in status:
					break

				# if file no longer exists stop daemon.
				if not os.path.exists(self.path): 
					self.crash(f"ssht00ls daemon ({self.id}): Mounted directory [{self.path}] from [{self.alias}:{self.remote}] no longer exists.")

				# sync.
				response = self.sync()
				if self.log_level >= 1:
					r3sponse.log(response=response)
				if not response.success: 
					self.crash(f"ssht00ls daemon ({self.id}) error: {response.error}")

				# sleep.
				time.sleep(self.sleeptime)

			# stop.
			self.stop()

			#
		def stop():
			response = self.unmount()
			if not response["success"]: self.crash(f"ssht00ls daemon ({self.id}) error: {response['error']}")
			cache.set(id=self.path, data="*stopped*", group="daemons")
			if self.log_level >= 0: print(f"Stopped daemon {self.id}")
		def crash(self, error=None, response=None):
			response = self.unmount()
			if not response["success"]: 
				cache.set(id=self.path, data="*crashed*", group="daemons")
				raise ValueError(f"ssht00ls daemon ({self.id}) error: {response['error']}")
			if response != None: error = response["error"]
			cache.set(id=self.path, data="*crashed*", group="daemons")
			raise ValueError(error)
		def unmount(self):
			if os.path.exists(self.path):
				response = self.sync()
				if not response.success: return response
				cache.set(id=self.path, data="*unmounting*", group="daemons")
				time.sleep(1)
				response = self.delete(self.path, remote=False, subpath=False,)
				if not response.success: return response
			return r3sponse.success_response("Successfully unmounted.")
		def index(self, short=False):

			# index.
			remote_response = ssync.index(path=self.path, alias=self.alias, checks=False)
			if not remote_response["success"]:  return remote_response
			response = ssync.index(path=self.path)
			if not response["success"]:  return response
			index, remote_index, clean_index, remote_clean_index = response["index"], remote_response["index"], {}, {}
			all_paths = []
			for path in list(index.keys()):
				subpath = self.subpath(path)
				if subpath not in all_paths: all_paths.append(subpath)
				clean_index[subpath] = index[path]
			for path in list(remote_index.keys()):
				subpath = self.subpath(path)
				if subpath not in all_paths: all_paths.append(subpath)
				remote_clean_index[subpath] = remote_index[path]
			synchronized = clean_index == remote_clean_index
			#print(f'clean_index: {json.dumps(clean_index,indent=4)}, remote_clean_index: {json.dumps(remote_clean_index,indent=4)}')
			if short in ["automatic", "auto"]:
				if not synchronized: short = False
			if short:
				return r3sponse.success_response(f"Successfully indexed [{self.alias}:{self.path}] & [{self.path}].", {
					"synchronized":synchronized,
					"index":index,
					"remote_index":remote_index,
				})
			else: return self.process_index(index, remote_index, all_paths)

		def process_index(self, index, remote_index, paths):

			# iterate.
			updates, deletions = {}, {}
			for path in paths:

				# vars.
				directory = " (d)" in path
				path = path.split(" (d)")[0]
				fullpath = self.fullpath(path)
				try: lmtime = index[fullpath]
				except KeyError: lmtime = None
				try: rmtime = remote_index[fullpath]
				except KeyError: rmtime = None
				try: last_lmtime = self.last_index[fullpath]
				except KeyError: last_lmtime = None
				try: last_rmtime = self.last_remote_index[fullpath]
				except KeyError: last_rmtime = None

				# wanted vars.
				local_to_remote, remote_to_local = False, False
				options = []
				
				# should not happen.
				if rmtime == None and lmtime == None: 
					self.last_index, self.last_remote_index = index, remote_index
					return r3sponse.error_response(f"No remote & local modification time present. (path: {path}), (rmtime: {rmtime}), (lmtime: {lmtime}), (last_rmtime: {last_rmtime}), (last_lmtime: {last_lmtime}), full index: {json.dumps(index,indent=4)}.")

				# one missing.
				elif rmtime == None or lmtime == None:
					
					# local created a file.
					if rmtime == None and lmtime != None and last_lmtime == None:
						local_to_remote = True

					# local deleted a file.
					elif rmtime != None and lmtime == None and last_lmtime != None:
						local_to_remote = True
						options.append("delete")

					# remote created a file.
					elif rmtime != None and lmtime == None and last_lmtime == None:
						remote_to_local = True

					# remote deleted a file.
					elif rmtime == None and lmtime != None and last_lmtime != None:
						remote_to_local = True
						options.append("delete")

					# should not happen.
					else:
						self.last_index, self.last_remote_index = index, remote_index
						return r3sponse.error_response(f"Should not happen (#3243443). (path: {path}), (rmtime: {rmtime}), (lmtime: {lmtime}), (last_rmtime: {last_rmtime}), (last_lmtime: {last_lmtime}), full index: {json.dumps(index,indent=4)}.")

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
						self.last_index, self.last_remote_index = index, remote_index
						return r3sponse.error_response(f"Unable to compare rmtime: {rmtime} & lmtime: {lmtime}. (path: {path}), (rmtime: {rmtime}), (lmtime: {lmtime}), (last_rmtime: {last_rmtime}), (last_lmtime: {last_lmtime}), full index: {json.dumps(index,indent=4)}.")

				# should not happen.
				else:
					self.last_index, self.last_remote_index = index, remote_index
					return r3sponse.error_response(f"Should not happen (#27834628). (path: {path}), (rmtime: {rmtime}), (lmtime: {lmtime}), (last_rmtime: {last_rmtime}), (last_lmtime: {last_lmtime}), full index: {json.dumps(index,indent=4)}.")

				# add to updates.
				if local_to_remote and remote_to_local:
					self.last_index, self.last_remote_index = index, remote_index
					return r3sponse.error_response(f"Can not synchronize both remote to local & local to remote (rmtime: {rmtime}) (lmtime: {lmtime}), (last_rmtime: {last_rmtime}) (last_lmtime: {last_lmtime}), full index: {json.dumps(index,indent=4)}.")
				if "delete" in options: 
					if self.log_level >= 1: 
						if local_to_remote:
							print(f"Deletion required {path} {self.alias}:{path} (rmtime: {rmtime}) (lmtime: {lmtime})")
						else:
							print(f"Deletion required {self.alias}:{path} {path} (rmtime: {rmtime}) (lmtime: {lmtime})")
					deletions[path] = {
						"options":options,
						"remote_to_local":remote_to_local,
						"local_to_remote":local_to_remote,
						"directory":directory,}
				elif remote_to_local or local_to_remote:
					if self.log_level >= 1: 
						if local_to_remote:
							print(f"Update required {path} {self.alias}:{path} (rmtime: {rmtime}) (lmtime: {lmtime})")
						else:
							print(f"Update required {self.alias}:{path} {path} (rmtime: {rmtime}) (lmtime: {lmtime})")
					updates[path] = {
						"options":options,
						"remote_to_local":remote_to_local,
						"local_to_remote":local_to_remote,
						"directory":directory,}
			# handler.
			self.last_index, self.last_remote_index = index, remote_index
			return r3sponse.success_response(f"Successfully indexed [{self.alias}:{self.path}] & [{self.path}].", {
				"synchronized":len(updates) == 0 and len(deletions) == 0,
				"updates":updates,
				"deletions":deletions,
				"index":index,
				"remote_index":remote_index,
			})
		def local_to_remote(self, path, info, directory=False, forced=False, delete=False):
			if self.log_level >= 0: print(f"Synchronizing {path} to {self.alias}:{path} (delete: {delete}) (forced: {forced}).")
			return self.ssync.push(
				path=self.fullpath(path, append_slash=directory), 
				alias=self.alias, 
				remote=self.fullpath(path, remote=True, append_slash=directory), 
				directory=directory,
				delete=delete,
				forced=forced,
				safe=False,
				accept_new_host_keys=True,
				checks=False,
				log_level=-1,)
		def remote_to_local(self, path, info, directory=False, forced=False, delete=False):
			if self.log_level >= 0: print(f"Synchronizing {self.alias}:{path} to {path} (delete: {delete}) (forced: {forced}).")
			return self.ssync.pull(
				path=self.fullpath(path, append_slash=directory), 
				alias=self.alias, 
				remote=self.fullpath(path, remote=True, append_slash=directory), 
				directory=directory,
				delete=delete,
				forced=forced,
				safe=False,
				accept_new_host_keys=True,
				checks=False,
				log_level=-1,)
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
			if self.sandbox: 
				if remote:
					return r3sponse.success_response(f"Sandbox enabled, skip delettion of {self.alias}:{path}.")
				else:
					return r3sponse.success_response(f"Sandbox enabled, skip delettion of {path}.")

			# logs.
			if self.log_level >= 0:
				if remote: print(f"Deleting {self.alias}:{path}.")
				else:print(f"Deleting {path}.")

			# proceed.
			if subpath:
				path = self.fullpath(path, remote=remote)
			
			# local to remote.
			if remote:
				os.system(f"ssh {self.alias} ' printf 'y' | rm -fr {path} ' ")
				response = utils.test_ssh_path(alias=self.alias, path=path)
				if response.error != None and f"{path} does not exist" not in response.error:
					return r3sponse.error_response(f"Failed to delete {path}, error: {response.error}")
				return r3sponse.success_response(f"Successfully deleted {self.alias}:{path}")

			# remote to local.
			else:
				os.system(f"printf 'y' | rm -fr {path}")
				if os.path.exists(path):
					return r3sponse.error_response(f"Failed to delete {path}")
				return r3sponse.success_response(f"Successfully deleted {path}")
		def sync(self):

			# get index.
			response = self.index(short="auto")
			if not response.success: return response
			elif response.synchronized:
				return r3sponse.success_response(f"Directories [{self.alias}:{self.path}] & [{self.path}] are already synchronized.")
			updates,deletions = response.unpack(["updates", "deletions"])

			# iterate updates.
			dirs = {}
			for path, info in updates.items():
				if self.log_level >= 0: print(f"Updating {path}.")

				# local to remote.
				if info["local_to_remote"]:
					if info["directory"] in [True, "True", "TRUE", "true"]: dirs[path] = info
					else: self.local_to_remote(path, info)

				# remote to local.
				elif info["remote_to_local"]:
					#response = utils.test_ssh_dir(alias=self.alias, path=path)
					#if response.error != None and "is not a directory" in response.error: return response
					#elif response.success: dirs[path] = info
					if info["directory"] in [True, "True", "TRUE", "true"]: dirs[path] = info
					else: self.remote_to_local(path, info)

			# iterate excepted dirs.
			for path, info in dirs.items():

				# local to remote.
				if info["local_to_remote"]:
					self.local_to_remote(path, info, directory=True)

				# remote to local.
				elif info["remote_to_local"]:
					self.remote_to_local(path, info, directory=True)

			# push deletions.
			for path, info in deletions.items():
				remote = info["local_to_remote"] == True
				response = self.delete(path, remote=remote)
				if not response.success: return response

			# check synchronized index.
			response = self.index(short=True)
			if not response.success: return response
			elif not response.synchronized:
				if self.log_level <= 0:
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
					return r3sponse.error_response(f"Failed to synchronize [{self.alias}:{self.remote}] & [{self.path}], failed to update mismatches: {json.dumps(mismatches, indent=4)}].")

			# handler.
			return r3sponse.success_response(f"Successfully synchronized [{self.alias}:{self.path}] & [{self.path}].")

# initialized objects.
ssync = SSync()


#print(ssync.mount(
#	alias="dev.vandenberghinc.com",
#	remote="/tmp/testmount",
#	path="/tmp/testmount",))
#quit()