#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from syst3m.classes.config import *
from syst3m.classes import utils
from syst3m.classes.color import color, symbol

"""
missing imports / variables:
	defaults, python_plus
"""

# the user object.
class User(object):
	# notes about the object
	# this is an example
	def __init__(self, 
		# the users username.
		username=None,
	):

		# arguments.
		self.username = username
		self.home_directory = f"{HOME_BASE}{self.username}/"

		#
	def create(self):
		
		# initialize default response.
		response = utils.__default_response__()
		
		# check duplicates.
		l_response = self.check()
		if l_response["error"] != None: return l_response
		if l_response["exists"]:
			response["error"] = f"User [{self.username}] already exists."
			return response

		# check home dir.
		if os.path.exists(self.home_directory): 
			response["error"] = f"Home directory [{self.home_directory}] already exists."
			return response

		# handle linux.
		if OS in ["linux"]:
			#self.console.execute("sudo useradd -s /bin/bash -d {home_directory} -m {username} # for ubuntu".format(
			# ubuntu.
			output = utils.__execute__(
				command=["sudo", "useradd", "-s", "/bin/bash", "-m", self.username],)

			# success.
			if output == "":
				response["success"] = True
				response["message"] = f"Successfully created user [{self.username}]."
				return response

			else:
				response["error"] = Formats.String(output.replace("useradd: ", "").replace("\n", ". ")).capitalized_word()
				return response

		# handle macos.
		elif OS in ["macos"]:
			response["error"] = f"Unsupported operating system [{OS}]."
			return response

		
		

		#
	def delete(self):

		# initialize default response.
		response = utils.__default_response__()
		
		# check existance.
		l_response = self.check()
		if l_response["error"] != None: return l_response
		if not l_response["exists"]:
			response["error"] = f"User [{self.username}] does not exist."
			return response

		# handle linux.
		if OS in ["linux"]:

			# delete.
			os.system(f"sudo userdel -r {self.username}")
			os.system(f"sudo rm -fr {self.home_directory}")

		# handle macos.
		elif OS in ["macos"]:
			response["error"] = f"Unsupported operating system [{OS}]."
			return response

		# check.
		l_response = self.check()
		if l_response["error"] != None: return l_response
		
		# success.
		if not l_response["exists"]:
			response["success"] = True
			response["message"] = f"Successfully deleted user [{self.username}]."
			return response
		else:
			response["error"] = f"Failed to delete user [{self.username}]."
			return response

		#
	def check(self, silent=False):

		# handle linux.
		response = utils.__default_response__()
		exists = False
		if OS in ["linux"]:
			try: 
				output = subprocess.check_output("sudo id {username}".format(username=self.username), shell=True).decode()
				exists = True
			except: exists = False

		# handle macos.
		elif OS in ["macos"]:
			response["error"] = f"Unsupported operating system [{OS}]."
			return response

		# success.
		response["exists"] = exists
		response["success"] = True
		response["message"] = f"Successfully checked user [{self.username}]."
		return response

		#
	def set_password(self, password=None):
		
		# check params.
		success, response = utils.__check_parameters__(empty_value=None, parameters={
			"password":password,
		})
		if not success: return response

		# handle linux.
		response = utils.__default_response__()
		if OS in ["linux"]:

			# get output.
			output = utils.__execute_script__(f"export HISTIGNORE='*sudo -S*' && echo '{password}\n{password}\n' | sudo -S -k sudo passwd {self.username}")
			
			# success.
			if "password updated successfully" in output:
				response["success"] = True
				response["message"] = f"Successfully edited the password of user [{self.username}]."
				return response

			# fail.
			else:
				response["error"] = f"Failed to edit the password of user [{self.username}]."
				return response

		# handle macos.
		elif OS in ["macos"]:
			response["error"] = f"Unsupported operating system [{OS}]."
			return response

		#
	def add_groups(self, groups=[]):

		# iterate groups.
		response = utils.__default_response__()
		for group in groups:

			# init group.
			group = GroupObject(name=group)

			# check existance.
			l_response = group.check()
			if l_response["error"] != None: return l_response
			if not response["exists"]: 
				response["error"] = f"Group [{group.name}] does not exist."
				return response

			# add user.
			l_response = group.add_users(users=[self.username])
			if l_response["error"] != None: return l_response

			#
		
		# success.
		response["success"] = True
		response["error"] = f"Successfully added user to [{len(groups)}] groups."
		return response

		#
	def delete_groups(self, groups=[]):
		
		# iterate groups.
		response = utils.__default_response__()
		for group in groups:
			group = GroupObject(name=group)
			l_response = group.check()
			if l_response["error"] != None: return l_response
			if not response["exists"]: 
				response["error"] = f"Group [{group.name}] does not exist."
				return response

			# delete user.
			l_response = group.delete_users(users=[self.username])
			if l_response["error"] != None: return l_response

				
		# success.
		response["success"] = True
		response["error"] = f"Successfully added user to [{len(groups)}] groups."
		return response

		#

# the group object.
class Group(object):
	def __init__(
		self, 
		# string format.
		name=None,
		users=[], # all authorized user identifiers.
		# boolean format.
		get_users=False, # (only gets filled if the storages group exists.)
	):

		# arguments.
		self.name = name
		self.users = users

		# functions.
		if get_users:
			response = self.check()
			if response["success"] and response["exists"]:
				response = self.list_users()
				if response["success"]: self.users = response["users"]

		#
	def create(self, users=None):

		# initialize default response.
		if users == None: users = self.users
		response = utils.__default_response__()

		# check existance.
		l_response = self.check()
		if l_response["error"] != None: return l_response
		elif l_response["exists"]:
			response["error"] = f"Group [{self.name}] already exists."
			return response

		# handle linux.
		if OS in ["linux"]:
			output = utils.__execute__(
				command=["sudo", "groupadd", self.name],)

			# success.
			if output == "":
				response["success"] = True
				response["message"] = f"Successfully created group [{self.name}]."
				return response

			else:
				response["error"] = Formats.String(output.replace("groupadd: ", "").replace("\n", ". ")).capitalized_word()
				return response

		# handle macos.
		elif OS in ["macos"]:
			response["error"] = f"Unsupported operating system [{OS}]."
			return response

		#
	def delete(self):
		
		# initialize default response.
		response = utils.__default_response__()

		# check existance.
		l_response = self.check()
		if l_response["error"] != None: return l_response
		elif l_response["exists"]:
			response["error"] = f"Group [{self.name}] already exists."
			return response

		# handle linux.
		if OS in ["linux"]:
			os.system(f"sudo groupdel {self.name}")

		# handle macos.
		elif OS in ["macos"]:
			response["error"] = f"Unsupported operating system [{OS}]."
			return response

		# check existance.
		l_response = self.check()
		if l_response["error"] != None: return l_response
		elif l_response["exists"]:
			response["error"] = f"Failed to delete group [{self.name}]."
			return response
		else:
			response["success"] = True
			response["message"] = f"Successfully deleted group [{self.name}]."
			return response


		#
	def check(self):
		
		# initialize response.
		response = utils.__default_response__()

		# handle linux.
		exists = False
		if OS in ["linux"]:
			try:
				output = subprocess.check_output("grep '^{name}' /etc/group".format(name=self.name), shell=True).decode()
				exists = True
			except: exists = False

		# handle macos.
		elif OS in ["macos"]:
			response["error"] = f"Unsupported operating system [{OS}]."
			return response

		
		# success.
		response["exists"] = exists
		response["success"] = True
		response["message"] = f"Successfully checked group [{self.name}]."
		return response

		#
	def list_users(self):

		# initialize default response.
		response = utils.__default_response__()

		# check existance.
		l_response = self.check()
		if l_response["error"] != None: return l_response
		elif not l_response["exists"]:
			response["error"] = f"Group [{self.name}] does not exists."
			return response

		# handle linux.
		users = []
		if OS in ["linux"]:
			try: output = subprocess.check_output("members "+self.name, shell=True).decode().replace("\n", "").split(" ")
			except: output = []
			for i in output:
				if i not in [""]: 
					users.append(i.replace("\n", ""))

		# handle macos.
		elif OS in ["macos"]:
			response["error"] = f"Unsupported operating system [{OS}]."
			return response

		# success.
		self.users = users
		response["users"] = users
		response["success"] = True
		response["message"] = f"Successfully listed all users {len(users)} of group [{self.name}]."
		return response

		#
	def delete_users(self, users=[]):
		
		# initialize default response.
		response = utils.__default_response__()

		# check existance.
		l_response = self.check()
		if l_response["error"] != None: return l_response
		elif not l_response["exists"]:
			response["error"] = f"Group [{self.name}] does not exists."
			return response

		# handle linux.
		if OS in ["linux"]:
			for user in users:
				output = utils.__execute__(
					command=["sudo", "deluser", user, self.name],)
				if output != "":
					response["error"] = Formats.String(output.replace("deluser: ", "").replace("\n", ". ")).capitalized_word()
					return response

		# handle macos.
		elif OS in ["macos"]:
			response["error"] = f"Unsupported operating system [{OS}]."
			return response

		# success.
		response["users"] = users
		response["success"] = True
		response["message"] = f"Successfully deleted {len(users)} users from group [{self.name}]."
		return response

		#
	def add_users(self, users=[]):

		# initialize default response.
		response = utils.__default_response__()

		# check existance.
		l_response = self.check()
		if l_response["error"] != None: return l_response
		elif not l_response["exists"]:
			response["error"] = f"Group [{self.name}] does not exists."
			return response

		# handle linux.
		if OS in ["linux"]:
			for user in users:
				output = utils.__execute__(
					command=["sudo", "usermod", "-a", "-G", self.name, user],)
				if output != "":
					response["error"] = Formats.String(output.replace("usermod: ", "").replace("\n", ". ")).capitalized_word()
					return response

		# handle macos.
		elif OS in ["macos"]:
			response["error"] = f"Unsupported operating system [{OS}]."
			return response

		# success.
		response["users"] = users
		response["success"] = True
		response["message"] = f"Successfully added {len(users)} users to group [{self.name}]."
		return response

		#
	def check_users(self, users=[]):
		# deletes all users that are not in the specified ones & adds new specified ones.
		#

		# initialize default response.
		response = utils.__default_response__()

		# check existance.
		l_response = self.check()
		if l_response["error"] != None: return l_response
		elif not l_response["exists"]:
			response["error"] = f"Group [{self.name}] does not exists."
			return response

		# handle linux.
		to_delete, to_add  = [], []
		if OS in ["linux"]:
			
			# check to delete:
			response = self.list_users()
			if response["error"] != None: return response
			l_users = response["users"]
			for user in l_users:
				if user not in users: to_delete.append(user)
			if len(to_delete) > 0:
				response = self.delete_users(users=to_delete)
				if response["error"] != None: return response

			# check to add:
			response = self.list_users()
			if response["error"] != None: return response
			l_users = response["users"]
			for user in users:
				if user not in l_users: to_add.append(user)
			if len(to_add) > 0:
				response = self.add_users(users=to_add)
				if response["error"] != None: return response

		# handle macos.
		elif OS in ["macos"]:
			response["error"] = f"Unsupported operating system [{OS}]."
			return response

		# success.
		response = utils.__default_response__()
		response["success"] = True
		response["message"] = f"Successfully added {len(to_add)} & removed {len(to_delete)} users from group [{self.name}]."
		return response

		#

"""
# the unix manager.
class UnixManager(object):
	# notes about the object
	# this is an example
	def __init__(self):

		# init:
		self.users_path = "/home/"
		if OS in ["macos"]: self.users_path = "/Users/"
		self.users = {} # can be filles with objects, format = {"$idenfitier":UserObject()}
		self.groups = {} # can be filles with objects, format = {"$idenfitier":GroupObject()}

"""






"""

# -----------------------
# the User() object class.

# initialize a user object.
user = User("testuser")

# check if the user exists.
response = user.check()
if response["success"]: print("User existance:",response["exists"])

# create a user.
response = user.create()

# delete a user.
response = user.delete()

# set a users password.
response = user.set_password(password="Doeman12!")

# add the user to groups.
response = user.add_groups(groups=[])

# delete the user from groups.
response = user.add_groups(groups=[])

# -----------------------
# the Group() object class.

# initialize a group object.
group = Group("testgroup")

# check if the group exists.
response = group.check()
if response["success"]: print("Group existance:",response["exists"])

# create a group.
response = group.create()

# delete a group.
response = group.delete()

# list the current users.
response = group.list_users()
if response["success"]: print(f"Users of group {group.name}:",response["users"])

# add users to the group.
response = group.add_users(users=["testuser"])

# delete users from the group.
response = group.delete_users(users=["testuser"])

# check if specified users are enabled and remove all other users.
response = group.check_users(users=["testuser"])

# -----------------------
# The dictionary response.

# handle response.
if response["error"] != None: print(response["error"])
else: print(response["message"])

"""