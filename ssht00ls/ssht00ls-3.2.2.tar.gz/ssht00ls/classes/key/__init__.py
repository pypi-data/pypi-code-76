#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from ssht00ls.classes.config import *
from ssht00ls.classes import utils
from ssht00ls.classes.smart_cards import smart_cards

# the ssh key object class.
class Key(object):
	def __init__(self):

		# variables.
		a = 1

		#
	def edit_passphrase(self, path=None, old=None, new=None):

		# checks.
		response = r3sponse.check_parameters({
			"old":old,
			"new":new,
			"path":path,
		})
		if not response["success"]: return response
		
		# do.
		output = utils.__execute__(["ssh-keygen", "-p", "-P", old, "-N", new, "-f", path])

		# check fails.
		if "incorrect passphrase supplied" in output:
			response["error"] = f"Provided an incorrect passphrase for key [{path}]."
			return response
		elif "No such file or directory" in output:
			response["error"] = f"Key [{path}] does not exist."
			return response
		
		# check success.	
		elif "Your identification has been saved with the new passphrase" in output:
			response["success"] = True
			response["message"] = f"Successfully edited the passphrase of key [{path}]."
			return response

		# unknown.
		else:
			l = f"Failed to edit the passphrase of key [{path}]"
			response["error"] = (f"{l}, error: "+output.replace("\n", ". ").replace(". .", ".")+".)").replace(". .",".").replace("\r","").replace("..",".")
			return response

			
		
		#
	def edit_comment(self, path=None, passphrase=None, comment=None):

		# checks.
		response = r3sponse.check_parameters({
			"old":old,
			"passphrase":passphrase,
			"comment":comment,
		})
		if not response["success"]: return response
		
		# do.
		output = utils.__execute__(["ssh-keygen", "-c", "-P", passphrase, "-C", comment, "-f", path])

		# check fails.
		if "incorrect passphrase supplied" in output:
			response["error"] = f"Provided an incorrect passphrase for key [{path}]."
			return response
		elif "No such file or directory" in output:
			response["error"] = f"Key [{path}] does not exist."
			return response
		
		# check success.	
		elif "Comment '" in output and "' applied" in output:
			response["success"] = True
			response["message"] = f"Successfully edited the comment of key [{path}]."
			return response

		# unknown.
		else:
			l = f"Failed to edit the comment of key [{path}]"
			response["error"] = (f"{l}, error: "+output.replace("\n", ". ").replace(". .", ".")+".)").replace(". .",".").replace("\r","").replace("..",".")
			return response

			
		
		#
	def generate(self, path=None, passphrase=None, comment=""):

		# checks.
		directory = path
		if directory[len(directory)-1] != "/": return r3sponse.error_response("The path must be a directory and end with a [/].")
		response = r3sponse.check_parameters({
			"directory":directory,
		})
		if not response["success"]: return response

		# check arguments.
		if passphrase in [None, False]:
			passphrase = '""'

		# create dir.
		if os.path.exists(directory): 
			response["error"] = f"Key directory [{directory}] already exists."
			return response
		else:
			os.mkdir(directory)
			utils.__set_file_path_permission__(directory, permission=700, sudo=True)
			utils.__set_file_path_ownership__(directory, owner=os.environ.get("USER"), group=None, sudo=True)

		# options.
		private_key = f'{directory}/private_key'
		public_key = f'{directory}/public_key'
		identity_file = f'-f {private_key}'
		if comment == None: comment = ""
		if "[#id:" not in comment: comment += f" [#id:{utils.__generate_shell_string__(characters=48, numerical_characters=True, special_characters=True)}]"
		comment = '-C "{}"'.format(comment)
		passphrase = f'-N "{passphrase}"'#utils.__string_to_bash__(passphrase)

		# execute.
		os.system(f'ssh-keygen -q -v -o -a 100 -t ed25519 {passphrase} {identity_file} {comment}')
		if not os.path.exists(private_key): 
			utils.__delete_file_path__(directory, forced=True, sudo=True)
			response["error"] = f"Failed to generate key [{directory}]."
			return response

		# permissions.
		utils.__set_file_path_permission__(private_key, permission=600, sudo=True)
		utils.__set_file_path_ownership__(private_key, owner=os.environ.get("USER"), group=None, sudo=True)
		os.system(f"mv {private_key}.pub {public_key}")
		if not os.path.exists(public_key): 
			utils.__delete_file_path__(directory, forced=True, sudo=True)
			response["error"] = f"Failed to move private key [{private_key}]."
			return response
		utils.__set_file_path_permission__(public_key, permission=640, sudo=True)
		utils.__set_file_path_ownership__(public_key, owner=os.environ.get("USER"), group=None, sudo=True)

		# response.
		response["success"] = True
		response["message"] = f"Successfully generated key [{directory}]."
		return response

		#
	def check(self, username=None, public_keys=[], reversed=False):

		# check if already present.
		if username == None: username = OWNER
		ssh_dir = Formats.FilePath(f"{HOME_BASE}/{username}/.ssh/", check_existance=False)
		auth_keys = Formats.FilePath(f"{HOME_BASE}/{username}/.ssh/authorized_keys", check_existance=False)
		output = self.__load_keys__(username)
		for key in public_keys:
			key = key.replace("\n", "")
			if key not in [""]:
				if not reversed and key not in output:
					ssh_dir.permission.set(permission=700, sudo=True, silent=True) # silent for when non existant.
					auth_keys.permission.set(permission=600, sudo=True, silent=True) # silent for when non existant.
					auth_keys.ownership.set(owner=username, sudo=True)
					ssh_dir.ownership.set(owner=username, sudo=True)
					return r3sponse.error_response(f'Public key [{key}] is not activated.')
				if reversed and key in output:
					ssh_dir.permission.set(permission=700, sudo=True, silent=True) # silent for when non existant.
					auth_keys.permission.set(permission=600, sudo=True, silent=True) # silent for when non existant.
					auth_keys.ownership.set(owner=username, sudo=True)
					ssh_dir.ownership.set(owner=username, sudo=True)
					return r3sponse.error_response(f'Public key [{key}] is activated.')

		# set correct permission.
		ssh_dir.permission.set(permission=700, sudo=True, silent=True) # silent for when non existant.
		auth_keys.permission.set(permission=600, sudo=True, silent=True) # silent for when non existant.
		auth_keys.ownership.set(owner=username, sudo=True)
		ssh_dir.ownership.set(owner=username, sudo=True)

		# success.
		if not reversed:
			return r3sponse.success_response(f'Successfully confirmed that the specfied {len(public_keys)} public key(s) are activated.')
		else:
			return r3sponse.success_response(f'Successfully confirmed that the specfied {len(public_keys)} public key(s) are not activated.')
	def enable(self, username=None, public_keys=[]):

		# check if already present.
		if username == None: username = OWNER
		output = self.__load_keys__(username)
		new_keys = []
		for key in public_keys:
			key = key.replace("\n", "")
			if key not in [""]:
				if key not in output:
					output.append(key)
		self.__save_keys__(username, output)

		# check if added.
		response = self.check(username, public_keys)
		if response["error"] != None: return response
	
		# success.
		return r3sponse.success_response(f'Successfully enabled {len(public_keys)} public key(s).')

		#
	def disable(self, username=None, public_keys=[]):

		# check if already present.
		if username == None: username = OWNER
		output = self.__load_keys__(username)
		new_keys = []
		for key in output:
			key = key.replace("\n", "")
			if key not in [""]:
				if key not in public_keys: new_keys.append(key)
		self.__save_keys__(username, new_keys)

		# check if added.
		response = self.check(username, public_keys, reversed=True)
		if response["error"] != None: return response
	
		# success.
		return r3sponse.success_response(f'Successfully disabled {len(public_keys)} public key(s).')

		#
	def __load_keys__(self, username):

		# make readable.
		if username == None: username = OWNER
		sudo = OWNER != username or True
		ssh_dir = Formats.FilePath(f"{HOME_BASE}/{username}/.ssh/", check_existance=False)
		auth_keys = Formats.FilePath(f"{HOME_BASE}/{username}/.ssh/authorized_keys", check_existance=False)

		# checks.
		if not ssh_dir.exists(sudo=sudo):
			ssh_dir.create(
				directory=True,
				permission=770,
				owner=username,
				group=None,
				sudo=sudo,)
		if not auth_keys.exists(sudo=sudo):
			auth_keys.create(
				directory=False,
				data="",
				permission=770,
				owner=username,
				group=None,
				sudo=sudo,)

		ssh_dir.permission.set(permission=770, sudo=sudo, silent=True) # silent for when non existant.
		auth_keys.permission.set(permission=770, sudo=sudo, silent=True) # silent for when non existant.
		auth_keys.ownership.set(owner=OWNER, sudo=sudo)
		ssh_dir.ownership.set(owner=OWNER, sudo=sudo)

		if sudo: command = ["sudo"]
		else: command = []
		output = utils.__execute__(command + ["cat", f"{HOME_BASE}/{username}/.ssh/authorized_keys"], return_format="array")
		return output

		#
	def __save_keys__(self, username, public_keys):

		# make readable.
		if username == None: username = OWNER
		sudo = OWNER != username or True
		ssh_dir = Formats.FilePath(f"{HOME_BASE}/{username}/.ssh/", check_existance=False)
		auth_keys = Formats.FilePath(f"{HOME_BASE}/{username}/.ssh/authorized_keys", check_existance=False)

		# checks.
		if not ssh_dir.exists(sudo=sudo):
			ssh_dir.create(
				directory=True,
				permission=770,
				owner=username,
				group=None,
				sudo=sudo,)
		if not auth_keys.exists(sudo=sudo):
			auth_keys.create(
				directory=False,
				data="",
				permission=770,
				owner=username,
				group=None,
				sudo=sudo,)

		f = Files.File(path="/tmp/file")
		new = []
		for public_key in public_keys:
			new.append(public_key.replace("\n",''))
		f.save(Files.Array(path=False, array=new).string(joiner="\n"))
		os.system(f"sudo mv {f.file_path.path} {auth_keys.path}")

		ssh_dir.permission.set(permission=700, sudo=sudo, silent=True) # silent for when non existant.
		auth_keys.permission.set(permission=600, sudo=sudo, silent=True) # silent for when non existant.
		auth_keys.ownership.set(owner=OWNER, sudo=sudo)
		ssh_dir.ownership.set(owner=OWNER, sudo=sudo)

		#

# Initialized classes.
key = Key()

"""

# --------------------
# SSH Key.

# generate a key.
response = key.generate(path="/path/to/mykey/", passphrase="passphrase123!", comment="my key")

# edit the passphrase of a key.
response = key.edit_passphrase(path="/path/to/mykey/private_key", new="Passphrase123!", old="passphrase123!")

"""






