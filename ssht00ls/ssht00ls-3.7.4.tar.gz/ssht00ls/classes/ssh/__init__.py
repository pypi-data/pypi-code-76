#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from ssht00ls.classes.config import *
import ssht00ls.classes.ssh.utils as ssh_utils 

# the ssh object class.
class SSH(object):
	def __init__(self):
		self.utils = ssh_utils
	def session(self, 
		alias=None,
	):
		response = r3sponse.check_parameters({
			"alias":alias,
		})
		if not response.success: return response
		os.system(f"ssh {DEFAULT_SSH_OPTIONS} {alias}")
		return r3sponse.success(f"Successfully started ssh session [{alias}].")
	def command(self,
		# the alias.
		alias=None,
		# the command to execute.
		command=None,
		# serialize the output to json.
		serialize=False,
		# the log level.
		log_level=0,
	):
		response = r3sponse.check_parameters({
			"alias":alias,
			"command":command,
		})
		if not response.success: return response
		response = self.utils.execute(
			command=f"""ssh {DEFAULT_SSH_OPTIONS} {alias} ' {command} ' """,
			message=f"Successfully executed the command on remote [{alias}].",
			error=f"Failed to execute the command on remote [{alias}].",
			log_level=log_level,
			get_output=True,
			serialize=serialize,)
		if response.success: 
			print(response.output)
		else:
			print(response.error)
		return response
		
# initialized objects.
ssh = SSH()