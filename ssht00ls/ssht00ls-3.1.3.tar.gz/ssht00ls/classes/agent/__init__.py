#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from ssht00ls.classes.config import *
from ssht00ls.classes import utils
from ssht00ls.classes.smart_cards import smart_cards
from ssht00ls.classes.ssh import ssh

# the ssh agent object class.
class Agent(object):
	def __init__(self):

		# variables.
		#self.initialize()
		
		"""# set agent.
		self.SSH_AUTH_SOCK = os.environ.get("SSH_AUTH_SOCK")
		self.SSH_AGENT_PID = os.environ.get("SSH_AGENT_PID")
		if self.SSH_AUTH_SOCK == None or self.SSH_AGENT_PID == None:
			output = subprocess.check_output(["ssh-agent"]).decode()
			self.SSH_AUTH_SOCK = output.split("SSH_AUTH_SOCK=")[1].split(";")[0]
			self.SSH_AGENT_PID = output.split("SSH_AGENT_PID=")[1].split(";")[0]
			os.environ["SSH_AUTH_SOCK"] = self.SSH_AUTH_SOCK
			os.environ["SSH_AGENT_PID"] = self.SSH_AGENT_PID

		# set agent nr.2.
		try:
			output = utils.__execute__([f"ssh-add", "-D"])
		except: a=1
		try:
			output = utils.__execute__([f"ssh-add", "-k"])
		except: a=1
		try:
			output = utils.__execute__(f"ssh-agent")
			try: 
				SSH_AUTH_SOCK = output.split("SSH_AUTH_SOCK=")[1].split(";")[0]
				os.environ["SSH_AUTH_SOCK"] = SSH_AUTH_SOCK
			except: a=1
			try: 
				SSH_AGENT_PID = output.split("SSH_AGENT_PID=")[1].split(";")[0]
				os.environ["SSH_AGENT_PID"] = SSH_AGENT_PID
			except: a=1
		except: a=1
		"""

		# set agent.
		if INTERACTIVE:
			ssh.utils.ssh_agent()
		#if self.SSH_AUTH_SOCK == None or self.SSH_AGENT_PID == None:
		#	utils.__execute_script__("pkill -9 -f ssh-agent")
		#	output = subprocess.check_output(["ssh-agent"]).decode()
		#	self.SSH_AUTH_SOCK = output.split("SSH_AUTH_SOCK=")[1].split(";")[0]
		#	self.SSH_AGENT_PID = output.split("SSH_AGENT_PID=")[1].split(";")[0]
		#	utils.__execute_script__("ssh-add -D")

		# set agent nr.2.
		#try:
		#	output = utils.__execute__([f"ssh-add", "-D"])
		#except: a=1
		#try:
		#	output = utils.__execute__([f"ssh-add", "-k"])
		#except: a=1
		#try:
		#	output = utils.__execute__(f"ssh-agent")
		#	try: 
		#		SSH_AUTH_SOCK = output.split("SSH_AUTH_SOCK=")[1].split(";")[0]
		#		os.environ["SSH_AUTH_SOCK"] = SSH_AUTH_SOCK
		#	except: a=1
		#	try: 
		#		SSH_AGENT_PID = output.split("SSH_AGENT_PID=")[1].split(";")[0]
		#		os.environ["SSH_AGENT_PID"] = SSH_AGENT_PID
		#	except: a=1
		#except: a=1

		
		#
	def add(self, 
		# the keys path.
		path=None, 
		# the keys passphrase.
		passphrase=None, 
		# enable if you are using a smart card.
		smart_card=False, 
		# the smart cards pin code
		pin=None, 
		# default timeout (do not use).
		timeout=0.5,
		# reattempt (do not use).
		reattempt=True,
	):

		# initialize.
		path = path.replace("//", "/")
		response = r3sponse.check_parameters(empty_value=None, parameters={
			"path":path
		})
		if not response["success"]: return response
		if smart_card:
			response = r3sponse.check_parameters(empty_value=None, parameters={
				"pin":pin
			})
			if not response["success"]: return response
		else:
			if not os.path.exists(path):
				return r3sponse.error_response(f"Key path [{path}] does not exist.")

		# check agent connection.
		output = utils.__execute__(["ssh-add", "-L"])
		if "Failed to communicate" in output or "agent refused operation" in output or "Error connecting to agent" in output or "Connection refused" in output:
			if reattempt:
				ssh.utils.ssh_agent()
				return self.add(
					# the keys path.
					path=path,
					# the keys passphrase.
					passphrase=passphrase,
					# enable if you are using a smart card.
					smart_card=smart_card,
					# the smart cards pin code
					pin=pin,
					# default timeout (do not use).
					timeout=timeout,
					# reattempt (do not use).
					reattempt=False,
				)
			else:
				return r3sponse.error_response("Failed to communicate with the ssh-agent. Try logging out the current system user & logging back in (or execute [$ eval `ssh-agent`]).")

		# with passphrase.
		if smart_card or passphrase != None:
			#self.initialize()
			if smart_card:
				path = smart_cards.path
				if OS in ["macos"]:
					os.system(f"rm -fr {smart_cards.path}")
					os.system(f"cp {smart_cards.original_path} {smart_cards.path}")
					os.system(f"chmod 644 {smart_cards.path}")
				#file = Files.File(path="/tmp/shell.sh")
				#file.save(f'export SSH_AUTH_SOCK={self.SSH_AUTH_SOCK}\nexport SSH_AGENT_PID={self.SSH_AGENT_PID}\nssh-add -e {path}\nssh-add -s {path}')
				#file.save(f'ssh-add -e {path}\nssh-add -s {path}')
				#file.save(f'ssh-add -s {path}')
				#file.file_path.permission.set(755)
				#spawn = pexpect.spawn(f'sh {file.file_path.path}')
				#file.file_path.delete(forced=True)
				#spawn = pexpect.spawn(f'ssh-add -e {path} && ssh-add -s {path}')
				try:
					output = subprocess.check_output([f"ssh-add", "-e", f"{path}"])
					print("remove card output:",output)
				except: a=1
				spawn = pexpect.spawn(f'ssh-add -s {path}')
			else:
				#file = Files.File(path="/tmp/shell.sh")
				#file.save(f'export SSH_AUTH_SOCK={self.SSH_AUTH_SOCK}\nexport SSH_AGENT_PID={self.SSH_AGENT_PID}\nssh-add {path}')
				#file.file_path.permission.set(755)
				#spawn = pexpect.spawn(f'sh {file.file_path.path}')
				#file.file_path.delete(forced=True)
				spawn = pexpect.spawn(f'ssh-add {path}')

			# send lines.
			output = None
			try:

				# handle pincode.
				if smart_card:
					spawn.expect(
						f'Enter passphrase for PKCS#11:',
						timeout=timeout,
					)
					spawn.sendline(str(pin))
				
				# handle pass.
				else:
					spawn.expect(
						f'Enter passphrase for {path}:',
						timeout=timeout,
					)
					spawn.sendline(passphrase)

			except pexpect.exceptions.TIMEOUT:
				a=1
			except pexpect.exceptions.EOF:
				a=1
			
			# handle output.
			output = spawn.read().decode()

			# check success.
			if "incorrect passphrase" in output.lower():
				return r3sponse.error_response("Provided an incorrect passphrase.")
			elif "incorrect pin" in output.lower():
				return r3sponse.error_response("Provided an incorrect pin code.")
			elif "Failed to communicate" in output or "agent refused operation" in output or "Error connecting to agent" in output or "Connection refused" in output:
				if reattempt:
					ssh.utils.ssh_agent()
					return self.add(
						# the keys path.
						path=path,
						# the keys passphrase.
						passphrase=passphrase,
						# enable if you are using a smart card.
						smart_card=smart_card,
						# the smart cards pin code
						pin=pin,
						# default timeout (do not use).
						timeout=timeout,
						# reattempt (do not use).
						reattempt=False,
					)
				else:
					return r3sponse.error_response("Failed to communicate with the ssh-agent. Try logging out the current system user & logging back in (or execute [$ eval `ssh-agent`]).")
			elif "Identity added:" in output or "Card added:" in output: 
				return r3sponse.success_response(f"Successfully added key [{path}] to the ssh agent.")
			elif output != "": 
				return r3sponse.error_response(f"Failed to add key [{path}] to the ssh agent, error: {output}")
			else: 
				return r3sponse.error_response(f"Failed to add key [{path}] to the ssh agent.")

			# handle eof.
			"""try:
				spawn.expect(pexpect.EOF, timeout=timeout)
			except pexpect.ExceptionPexpect as epe:
				return r3sponse.error_response(f"Failed to add key [{path}] to the ssh agent #3.")"""

		# without pass.
		else:
			output = utils.__execute__(command=["ssh-add", path], shell=False, timeout=timeout)

			# check success.
			if "Failed to communicate" in output or "agent refused operation" in output or "Error connecting to agent" in output or "Connection refused" in output:
				return r3sponse.error_response("Failed to communicate with the ssh-agent.")
			elif "Identity added:" in output: 
				return r3sponse.success_response(f"Successfully added key [{path}] to the ssh agent.")
			else: 
				return r3sponse.error_response(f"Failed to add key [{path}] to the ssh agent.")

		#
	def delete(self):

		# delete keys.
		output = utils.__execute__(command=["ssh-add", "-D"])

		# check success.
		if "Could not open a connection to your authentication agent." in output:
			return r3sponse.error_response("Failed to communicate with the ssh-agent.")
		elif "All identities removed." in output: 
			return r3sponse.success_response(f"Successfully removed all keys from the ssh agent.")
		else: 
			return r3sponse.error_response(f"Failed to remove all keys from the ssh agent.")

		#
	def list(self):
		# initialize.
		keys = []

		# list keys.
		output = utils.__execute__(command=["ssh-add", "-L"], return_format="array")
		if "Failed to communicate" in output:
			return r3sponse.error_response("Failed to communicate with the ssh-agent.")
		elif "The agent has no identities." in output:
			keys = []
		else:
			keys = output
		return r3sponse.success_response(f"Successfully listed the agent's keys.", {
			"keys":keys,
		})

		#
	def check(self, public_key=None, raw=False):


		# params.
		response = r3sponse.check_parameters({
			"public_key":public_key
		})
		if not response["success"]: return response

		# checks.
		if not raw and not os.path.exists(public_key):
			return r3sponse.error_response(f"Public key path [{public_key}] does not exist.")

		# load public key.
		if not raw:
			try:
				public_key = utils.__load_file__(public_key)
			except:
				return r3sponse.error_response(f"Failed to load public key path [{public_key}].")

		# retrieve id from public key.
		"""
		try:
			public_key_id = public_key.split("[#id:")[1].split("]")[0]
		except IndexError:
			return r3sponse.error_response(f"Public key [{public_key}] does not contain any id.")

		# list.
		response = self.list()
		if response["error"] != None: return response
		success = False
		for key in response["keys"]:
			try:
				l_id = key.split("[#id:")[1].split("]")[0]
				if l_id == public_key_id:
					success = True 
					break
			except IndexError: a=1
		"""

		# list.
		response = self.list()
		if response["error"] != None: return response
		success = False
		for key in response["keys"]:
			if public_key.replace("\n","") in key:
				success = True 
				break

		# success.
		if success:
			return r3sponse.success_response(f"Public key [{public_key}] is added to the ssh agent.")
		else:
			return r3sponse.error_response(f"Public key [{public_key}] is not added to the ssh agent.")

		#
	def initialize(self):

		# check communication.
		output = utils.__execute__(command=["ssh-add", "-l"])
		#print("DEBUG; initialize output ssh-add -l:",output)
		if "Failed to communicate" in output or "Error connecting to agent" in output:
			if not self.delete()["success"]:
				l = subprocess.check_output(['eval', '"$(ssh-agent)"'], shell=True).decode()
				output = utils.__execute__(command=["ssh-add", "-l"])
				if "Failed to communicate" in output or "Error connecting to agent" in output:
					return r3sponse.error_response("Failed to communicate with the ssh-agent.")
				else:
					output = utils.__execute__(command=["ssh-add", "-l"])
					if "Failed to communicate" in output or "Error connecting to agent" in output:
						return r3sponse.error_response("Failed to communicate with the ssh-agent.")
			else:
				output = utils.__execute__(command=["ssh-add", "-l"])
				if "Failed to communicate" in output or "Error connecting to agent" in output:
					return r3sponse.error_response("Failed to communicate with the ssh-agent.")

		# success.
		return r3sponse.success_response(f"Successfully initialized the ssh agent.")

# Initialized objects.
agent = Agent()

"""

# --------------------
# SSH Agent.

# initialize the ssh agent.
response = agent.initialize()

# delete all keys from the agent.
response = agent.delete()

# add a key to the agent.
response = agent.add(
	path="/path/to/mykey/private_key", 
	passphrase="TestPass!",)

# add a smart cards key to the agent.
response = agent.add(
	path=smart_card.path, 
	smart_card=True,
	pin=123456,)

# check if a key is added to the agent.
response = agent.check("/path/to/mykey/private_key")

# list all agent keys.
response = agent.list()

"""






