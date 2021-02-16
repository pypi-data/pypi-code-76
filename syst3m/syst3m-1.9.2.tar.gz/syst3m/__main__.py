#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# insert the package for universal imports.
import os, sys
from fil3s import Formats, Files

# only for cli:
from r3sponse import r3sponse

# settings.
SOURCE_NAME = "syst3m"
SOURCE_PATH = Formats.FilePath(__file__).base(back=1)
BASE = Formats.FilePath(SOURCE_PATH).base(back=1)
sys.path.insert(1, BASE)

# imports.
import syst3m
from syst3m.classes.config import *

# the cli object class.
class CLI(cl1.CLI):
	def __init__(self):
		
		# defaults.
		cl1.CLI.__init__(self,
			modes={
				"--user myuser":"Configure a system user (linux).",
				"    --check":"Check the existance of the specified user.",
				"    --create":"Create the specified user.",
				"    --delete":"Delete the specified user.",
				"    --password MyPassword":"Set the password of the specifed user (leave password blank for safe prompt).",
				"    --add-groups group1,group2":"Add the specified user to groups.",
				"    --delete-groups group1,group2":"Remove the specified user from groups.",
				"--group mygroup":"Configure a system group (linux).",
				"    --check":"Check the existance of the specified group.",
				"    --create":"Create the specified group.",
				"    --delete":"Delete the specified group.",
				"    --list-users":"List the users of the specified group.",
				"    --add-users user1,user2":"Add users from the specified group.",
				"    --delete-users user1,user2":"Delete users from the specified group.",
				"    --force-users user1,user2":"Add the specified users to the group and remove all others.",
				"--disk-space":"Get the free disk space (linux).",
				"--size /path/to/file":"Get the size of a file / directory (linux).",
				"-h / --help":"Show the documentation.",
			},
			options={
				"-c":"Do not clear the logs.",
			},
			alias=ALIAS,
			executable=__file__,
		)

		#
	def start(self):

		# clear logs.
		if not self.arguments.present(['-c']):
			os.system("clear")

		# help.
		if self.arguments.present(['-h', '--help']):
			print(self.documentation)

		# user.
		elif self.arguments.present(['--user']):
			syst3m.defaults.operating_system(supported=["linux"])

			# initialize a user object.
			user = syst3m.User(self.arguments.get("--user"))

			# check if the user exists.
			if self.arguments.present(['--check']):
				response = user.check()
				r3sponse.log(response)
				if r3sponse.success(response): print("User existance:",response["exists"])

			# create a user.
			elif self.arguments.present(['--create']):
				response = user.create()
				r3sponse.log(response)

			# delete a user.
			elif self.arguments.present(['--delete']):
				response = user.delete()
				r3sponse.log(response)

			# set a users password.
			elif self.arguments.present(['--password']):
				password = self.get_password(retrieve=True, message=f"Enter a new password of user [{user.username}]:")
				response = user.set_password(password=password)
				r3sponse.log(response)

			# add the user to groups.
			elif self.arguments.present(['--add-groups']):
				groups = self.arguments.get("--delete-groups").split(",")
				response = user.add_groups(groups=groups)
				r3sponse.log(response)

			# delete the user from groups.
			elif self.arguments.present(['--delete-groups']):
				groups = self.arguments.get("--delete-groups").split(",")
				response = user.add_groups(groups=groups)
				r3sponse.log(response)


			# invalid.
			else:  self.invalid()

		# group.
		elif self.arguments.present(['--group']):
			syst3m.defaults.operating_system(supported=["linux"])

			# initialize a group object.
			group = syst3m.Group(self.arguments.get("--group"))

			# check if the group exists.
			if self.arguments.present(['--check']):
				response = group.check()
				r3sponse.log(response)
				if r3sponse.success(response): 
					print("Group existance:",response["exists"])

			# create a group.
			elif self.arguments.present(['--create']):
				response = group.create()
				r3sponse.log(response)

			# delete a group.
			elif self.arguments.present(['--delete']):
				response = group.delete()
				r3sponse.log(response)

			# list the current users.
			elif self.arguments.present(['--list-users']):
				response = group.list_users()
				r3sponse.log(response)
				if r3sponse.success(response): 
					print(f"Users of group {group.name}:",response["users"])

			# add users to the group.
			elif self.arguments.present(['--add-users']):
				users = self.arguments.get("--add-users").split(",")
				response = group.add_users(users=users)
				r3sponse.log(response)

			# delete users from the group.
			elif self.arguments.present(['--delete-users']):
				users = self.arguments.get("--delete-users").split(",")
				response = group.delete_users(users=users)
				r3sponse.log(response)

			# check if the specified users are enabled and remove all other users.
			elif self.arguments.present(['--force-users']):
				users = self.arguments.get("--force-users").split(",")
				response = group.check_users(users=users)
				r3sponse.log(response)


			# invalid.
			else:  self.invalid()

		# free disk space.
		elif self.arguments.present(["--disk-space"]):
			syst3m.defaults.operating_system(supported=["linux"])
			import shutil
			import math
			def size(size_bytes):
			   if size_bytes == 0:
			       return "0B"
			   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
			   i = int(math.floor(math.log(size_bytes, 1024)))
			   p = math.pow(1024, i)
			   s = round(size_bytes / p, 2)
			   return "%s %s" % (s, size_name[i])
			total, used, free = shutil.disk_usage(__file__)
			print(f"total: {size(total)}, used: {size(used)}, free: {size(free)}")

		# size.
		elif self.arguments.present(["--size"]):
			fp = Formats.FilePath(self.arguments.get("--size"))
			if not fp.exists(): 
				print(f"File path [{fp.path}] does not exist.")
				sys.exit(1)
			else:
				loader = syst3m.console.Loader(f"Retrieving size of {fp.path} ...")
				size = fp.size()
				loader.stop()
				print(f"Size {fp.path}: {size}")

		# invalid.
		else:  self.invalid()

		#
	def invalid(self):
		print(self.documentation)
		print("Selected an invalid mode.")
		sys.exit(1)
	def get_password(self, retrieve=False, check=False, message="Password:"):
		password = self.arguments.get("--password", required=retrieve, default=None)
		if password == None:
			password = utils.__prompt_password__(message)
			if check and password != utils.__prompt_password__("Enter the same password:"):
				print("Passwords do not match.")
				sys.exit(1)
		else: password = password.replace("\\","").replace("\ ","")
		return password
# main.
if __name__ == "__main__":
	cli = CLI()
	if "--developer" in sys.argv:
		cli.start()
	else:
		try:
			cli.start()
		except KeyboardInterrupt:
			print("Aborted: KeyboardInterrupt")

