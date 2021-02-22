#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from fil3s.classes.config import *
import string
import time


# the syst3m.console.Loader object class (exact copy).
class Loader(threading.Thread):
	def __init__(self, message, autostart=True, log_level=0, interactive=True):
		threading.Thread.__init__(self)
		self.message = self.__clean_message__(message)
		self.last_message = str(self.message)
		self.log_level = log_level
		self.interactive = interactive
		if autostart and self.log_level >= 0: 
			if self.interactive:
				try:
					self.start()
				except KeyboardInterrupt as e:
					self.stop(success=False)
					raise KeyboardInterrupt(f"{e}")
			else:
				print(self.message+".")
	def run(self):
		if self.log_level >= 0: 
			self.running = True
			self.released = True
			while self.running:
				if not self.released:
					time.sleep(1)
				else:
					for i in ["|", "/", "-", "\\"]:
						if not self.released: break
						if self.message != self.last_message:
							print(self.__empty_message__(length=len(f"{self.last_message} ...   ")), end="\r")
							self.message = self.__clean_message__(self.message)
						print(f"{self.message} ... {i}", end="\r")
						self.last_message = self.message
						if not self.running: break
						time.sleep(0.33)
		self.running = "stopped"
	def stop(self, message=None, success=True, response=None, quiet=False):
		if self.log_level >= 0:
			if response == None:
				if message == None: message = self.message
			else:
				if response["error"] == None:
					message = response["message"]
				else:
					success = False
					message = "Error: "+response["error"]
			if self.interactive:
				self.running = False
				for i in range(120):
					if self.running == "stopped": break
					time.sleep(0.5)
				if self.running != "stopped": raise ValueError(f"Unable to stop loader [{self.message}].")
			if not quiet:
				if self.interactive:
					print(self.__empty_message__(length=len(f"{self.last_message} ...   ")), end="\r")
					if success:
						print(f"{message} ... done")
					else:
						print(f"{message} ... {color.red}failed{color.end}")
				else:
					if success:
						print(f"{message}. done")
					else:
						print(f"{message}. {color.red}failed{color.end}")
	def mark(self, new_message=None, old_message=None, success=True, response=None):
		if self.log_level >= 0: 
			if response != None:
				if response["error"] == None:
					success = True
				else:
					success = False
			if old_message == None: old_message = self.message
			if self.interactive:
				print(self.__empty_message__(length=len(f"{self.last_message} ...   ")), end="\r")
				if success:
					print(f"{old_message} ... done")
				else:
					print(f"{old_message} ... {color.red}failed{color.end}")
			else:
				if success:
					print(f"{old_message}. done")
				else:
					print(f"{old_message}. {color.red}failed{color.end}")
			if new_message != None: self.message = new_message
	def hold(self):
		if self.log_level >= 0: 
			self.released = False
			time.sleep(0.33)
	def release(self):
		if self.log_level >= 0: 
			self.released = True
			time.sleep(0.33)
	# system functions.
	def __clean_message__(self, message):
		if message[-len(" ..."):] == " ...": message = message[:-4]
		if message[-len("."):] == ".": message = message[:-1]
		if message[0].upper() != message[0]: message = message[1:]+message[0].upper()+message[1:]
		return color.fill(message)
	def __empty_message__(self, length=len("hello world")):
		s = ""
		for i in range(length): s += " "
		return s

# invalid os.
def __invalid_os__(os):
	raise OSError(f"Unsupported operating system [{os}].")
	#

# check memory only path.
def __check_memory_only__(path):
	if path == False: 
		raise ValueError("This object is only used in the local memory and is not supposed to be saved or loaded.")
	#

# the generate object.
class Generate(object):
	def __init__(self):
		a=1
	def pincode(self, length=6, charset=string.digits):
		return ''.join(random.choice(charset) for x in range(length))
		#
	def shell_string(self, length=6, numerical_length=False, special_length=False):
		charset = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
		for x in ast.literal_eval(str(charset)): charset.append(x.upper())
		if numerical_length:
			for x in [
				'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
			]: charset.append(x)
		if special_length:
			for x in [
				'-', '+', '_'
			]: charset.append(x)
		return ''.join(random.choice(charset) for x in range(length))
		#

# execute a shell command.
def __execute__(
	# the command in array.
	command=[],
	# wait till the command is pinished. 
	wait=False,
	# the commands timeout, [timeout] overwrites parameter [wait].
	timeout=None, 
	# the commands output return format: string / array.
	return_format="string", 
	# the subprocess.Popen.shell argument.
	shell=False,
	# pass a input string to the process.
	input=None,
):
	def __convert__(byte_array, return_format=return_format):
		if return_format == "string":
			lines = ""
			for line in byte_array:
				lines += line.decode()
			return lines
		elif return_format == "array":
			lines = []
			for line in byte_array:
				lines.append(line.decode().replace("\n","").replace("\\n",""))
			return lines

	# create process.
	if isinstance(command, str): command = command.split(' ')
	p = subprocess.Popen(
		command, 
		shell=shell,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		stdin=subprocess.PIPE,)
	
	# send input.
	if input != None:
		if isinstance(input, list):
			for s in input:
				p.stdin.write(f'{s}\n'.encode())
		elif isinstance(input, str):
			p.stdin.write(f'{input}\n'.encode())
		else: raise ValueError("Invalid format for parameter [input] required format: [string, array].")
		p.stdin.flush()
	
	# timeout.
	if timeout != None:
		time.sleep(timeout)
		p.terminate()
	
	# await.
	elif wait:
		p.wait()

	# get output.
	output = __convert__(p.stdout.readlines(), return_format=return_format)
	if return_format == "string" and output == "":
		output = __convert__(p.stderr.readlines(), return_format=return_format)
	elif return_format == "array" and output == []:
		output = __convert__(p.stderr.readlines(), return_format=return_format)
	return output
	
	
# default initialized classes.
generate = Generate()
