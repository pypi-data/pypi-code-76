#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from ssht00ls.classes.config import *
from ssht00ls.classes import utils

# the installation object class.
class Installation(object):
	def __init__(self):
		a=1
	def install(self, 
		# optional define the user (leave None for current user).
		username=None,
	):
		# initialize.
		response = utils.__default_response__()
		if username == None: username = OWNER
		home = f"{HOME_BASE}/{username}/"	
		sudo = True
		
		# users ssh directory.
		fp = Formats.FilePath(f"{home}.ssh/")
		if not fp.exists(sudo=sudo):
			fp.create(
				directory=True,
				permission=700,
				owner=username,
				group=None,
				sudo=sudo,)
		else:
			fp.permission.set(permission=700, sudo=sudo)
			fp.ownership.set(owner=username, group=None, sudo=sudo)

		# the ssh config.
		fp = Formats.FilePath(f"{home}.ssh/config")
		if not fp.exists(sudo=sudo):
			fp.create(
				directory=False,
				data="",
				permission=644,
				owner=username,
				group=None,
				sudo=sudo,)
		else:
			fp.permission.set(permission=644, sudo=sudo)
			fp.ownership.set(owner=username, group=None, sudo=sudo)

		# the ssh known hosts.
		fp = Formats.FilePath(f"{home}.ssh/known_hosts")
		if not fp.exists(sudo=sudo):
			fp.create(
				directory=False,
				data="",
				permission=644,
				owner=username,
				group=None,
				sudo=sudo,)
		else:
			fp.permission.set(permission=644, sudo=sudo)
			fp.ownership.set(owner=username, group=None, sudo=sudo)

		# authorized keys.
		fp = Formats.FilePath(f"{home}.ssh/authorized_keys")
		if not fp.exists(sudo=sudo):
			fp.create(
				directory=False,
				data="",
				permission=600,
				owner=username,
				group=None,
				sudo=sudo,)
		else:
			fp.permission.set(permission=600, sudo=sudo)
			fp.ownership.set(owner=username, group=None, sudo=sudo)

		# success.
		response["success"] = True
		response["message"] = f"Successfully installed ssh for user [{username}]."
		return response

		#
	def check_installed(self, 
		# optional define the user (leave None for current user).
		username=None,
	):	

		# initialize.
		response = utils.__default_response__()
		if username == None: username = OWNER
		home = f"{HOME_BASE}/{username}/"	
		sudo = True
		
		# users ssh directory.
		fp = Formats.FilePath(f"{home}.ssh/")
		if not fp.exists():
			response["error"] = f"Required ssh configuration file [{fp.path}] for user [{username}] is not installed."
			return response
		else:
			fp.permission.set(permission=700, sudo=sudo)
			fp.ownership.set(owner=username, group=None, sudo=sudo)

		# the ssh config.
		fp = Formats.FilePath(f"{home}.ssh/config")
		if not fp.exists():
			response["error"] = f"Required ssh configuration file [{fp.path}] for user [{username}] is not installed."
			return response
		else:
			fp.permission.set(permission=644, sudo=sudo)
			fp.ownership.set(owner=username, group=None, sudo=sudo)

		# the ssh known hosts.
		fp = Formats.FilePath(f"{home}.ssh/known_hosts")
		if not fp.exists():
			response["error"] = f"Required ssh configuration file [{fp.path}] for user [{username}] is not installed."
			return response
		else:
			fp.permission.set(permission=644, sudo=sudo)
			fp.ownership.set(owner=username, group=None, sudo=sudo)
			
		# authorized keys.
		fp = Formats.FilePath(f"{home}.ssh/authorized_keys")
		if not fp.exists():
			response["error"] = f"Required ssh configuration file [{fp.path}] for user [{username}] is not installed."
			return response
		else:
			fp.permission.set(permission=600, sudo=sudo)
			fp.ownership.set(owner=username, group=None, sudo=sudo)

		# success.
		response["success"] = True
		response["message"] = f"SSH is successfully installed for user [{username}]."
		return response
			
# Initialized objects.
installation = Installation()

"""

# --------------------
# SSH Installation.

# check if ssh is correctly installed.
# (leave the username None to use the current user.)
response = installation.check_installed(username=None)

# install the ssh correctly for the specified user.
if response["error"] != None:
	response = installation.install(username=None)

"""






