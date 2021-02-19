#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from fil3s.classes.config import *
import string
import time

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
