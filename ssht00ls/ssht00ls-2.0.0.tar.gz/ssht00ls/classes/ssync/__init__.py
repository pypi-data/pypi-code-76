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
		elif os.path.exists(path):
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
		if not r3sponse.success: return response

		# start daemon.
		p = subprocess.Popen(["python3", SOURCE_PATH, "--daemon", f"{alias}:{remote}", path, "--non-interactive"])

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
		elif not os.path.exists(path):
			return r3sponse.error_response(f"Path [{path}] does not exist.")
		elif not os.path.isdir(path):
			return r3sponse.error_response(f"Path [{path}] is not a directory.")
		elif "*mounted*" not in cache.get(id=path, group="daemons"):
			return r3sponse.error_response(f"Path [{path}] is not mounted.")
		path = utils.clean_path(path)

		# wait for daemon stop.
		response = self.stop_daemon(path=path)
		if not success: return response

		# delete local.
		"""
		if sudo: sudo_str = "sudo "
		else: sudo_str = ""
		os.system(f"{sudo_str}rm -fr {path}")
		if os.path.exists(path):
			return r3sponse.error_response(f"Failed to unmount [{path}].")
		"""

		# handler.
		return r3sponse.success_response(f"Successfully unmounted [{path}].")

		#
	def index(self, path=None, alias=None, log_level=0, accept_new_host_keys=True):

		# checks.
		if path == None:
			return r3sponse.error_response(f"Define parameter: path.")
		path = utils.clean_path(path)

		# remote.
		if alias != None:
			
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
			output = syst3m.utils.__execute_script__(f"printf 'yes' | ssh {alias} ' python3 /usr/local/lib/ssht00ls --index {path} --non-interactive ' ")
			try: response = json.loads(output)
			except Exception as e: 
				return r3sponse.error_response(f"Failed to serialize remote {alias} output: {output}")
			return r3sponse.ResponseObject(response)

		# local.
		else:
			if not os.path.exists(path):
				return r3sponse.error_response(f"Path [{path}] does not exist.")
			elif not os.path.isdir(path):
				return r3sponse.error_response(f"Path [{path}] is not a directory.")

			# index.
			index = {}
			for path in Files.Directory(path=path).paths(recursive=True):
				index[path] = Formats.FilePath(path).mtime(format="seconds")

			# handler.
			return r3sponse.success_response(f"Successfully indexed {len(index)} files from directory [{path}].", {
				"index":index,
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
		# update deleted files.
		delete=False,
		# forced mode.
		forced=False,
		# version control.
		safe=False,
		# accept new hosts keys.
		accept_new_host_keys=True,
		# log level.
		log_level=0,
	):	
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

		# pull.
		if exclude == None: exclude = self.exclude
		exclude_str = ""
		for i in exclude: exclude_str += f"--exclude {i} "
		delete_str = Formats.Boolean(delete).convert(true="--delete", false="")
		command = f"rsync -azP {alias}:{remote} {path} {exclude_str}{delete_str}"
		loader = syst3m.console.Loader(f"Pulling [{alias}:{remote}] to [{path}]")
		output = syst3m.utils.__execute_script__(command)
		if len(output) > 0 and output[len(output)-1] == "\n": output = output[:-1]
		cache.set(id=path, data="*mounted*", group="daemons")
		
		# handler.
		if "rsync: " in output or "rsync error: " in output:
			loader.stop(success=False)
			print(output)
			return r3sponse.success_response(f"Failed to pull [{alias}:{remote}] to [{path}].")
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
		# update deleted files.
		delete=False,
		# forced mode.
		forced=False,
		# version control.
		safe=False,
		# accept new hosts keys.
		accept_new_host_keys=True,
		# log level.
		log_level=0,
	):
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

		# push.
		if exclude == None: exclude = self.exclude
		exclude_str = ""
		for i in exclude: exclude_str += f"--exclude {i} "
		delete_str = Formats.Boolean(delete).convert(true="--delete", false="")
		command = f"rsync -azP {path} {alias}:{remote} {exclude_str}{delete_str}"
		loader = syst3m.console.Loader(f"Pushing [{path}] to [{alias}:{remote}].")
		output = syst3m.utils.__execute_script__(command)
		if len(output) > 0 and output[len(output)-1] == "\n": output = output[:-1]
		cache.set(id=path, data="*mounted*", group="daemons")
		
		# handler.
		if "rsync: " in output or "rsync error: " in output:
			loader.stop(success=False)
			print(output)
			return r3sponse.success_response(f"Failed to push [{path}] to [{alias}:{remote}].")
		else:
			loader.stop()
			return r3sponse.success_response(f"Successfully pushed [{path}] to [{alias}:{remote}].")


		#
	# the mounted daemon.
	def sync(self):
		for path in Files.Directory(path=f"{cache.path}/daemons/").paths(recursive=False):
			a=1
	def daemon(self, 
		# the ssh alias.
		alias=None, 
		# the remote path.
		remote=None, 
		# thel local path.
		path=None, 
		# settings.
		start=True,
	):
		path = utils.clean_path(path)
		remote = utils.clean_path(remote)
		daemon = self.Daemon({
			"alias":alias,
			"remote":remote,
			"path":path,
			"ssync":self,
		})
		if start: daemon.start()
		return daemon
	def stop_daemon(self, path, timeout=60, sleeptime=1):
		cache.set(id=path, data="*stop*", group="daemons")
		stopped = False
		for i in range(timeout/sleeptime):
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
			self.id = f"{self.alias}:{self.remote} ==> {self.path}"
		def run(self):

			# checks.
			if not os.path.exists(self.path):
				cache.set(id=self.path, data="*crashed*", group="daemons")
				raise ValueError(f"SSHT00ls daemon ({self.id}): Path [{self.path}] does not exist.")
			elif not os.path.isdir(self.path):
				cache.set(id=self.path, data="*crashed*", group="daemons")
				raise ValueError(f"SSHT00ls daemon ({self.id}): Path [{self.path}] is not a directory.")
			elif "*mounted*" not in cache.get(id=path, group="daemons"):
				cache.set(id=self.path, data="*crashed*", group="daemons")
				raise ValueError(f"SSHT00ls daemon ({self.id}): Path [{self.path}] is not mounted.")

			# check alias.
			response = aliases.check(alias)
			if not response.success: 
				cache.set(id=self.path, data="*crashed*", group="daemons")
				raise ValueError(response.error)

			# start.
			while True:

				# check stop command.
				if "*stop*" in cache.get(id=self.path, group="daemons"):
					break

				# if file no longer exists stop daemon.
				if not os.path.exists(self.path):
					cache.set(id=self.path, data="*crashed*", group="daemons")
					raise ValueError(f"SSHT00ls daemon ({self.id}): Mounted directory [{self.path}] from [{self.alias}:{self.remote}] no longer exists.")

			# stop.
			cache.set(id=self.path, data="*stopped*", group="daemons")

# initialized objects.
ssync = SSync()

path = "/tmp/testmount"
alias = "dev.vandenberghinc.com"
response = ssync.index(path=path, alias=alias)
print(response)
quit()

#print(ssync.mount(
#	alias="dev.vandenberghinc.com",
#	remote="/tmp/testmount",
#	path="/tmp/testmount",))
#quit()