#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from ssht00ls.classes.config import * 
import os, sys, requests, ast, json, pathlib, glob, string, getpass, django

# set a file path permission.
def __set_file_path_permission__(path, permission=755, sudo=False, recursive=False):
	if recursive: recursive = "-R "
	else: recursive = ""
	if sudo: sudo = "sudo "
	else: sudo = ""
	os.system(f"{sudo}chmod {recursive}{permission} {path}")
# set a file path ownership.
def __set_file_path_ownership__(path, owner=os.environ.get("USER"), group=None, sudo=False, recursive=False):
	if recursive: recursive = "-R "
	else: recursive = ""
	if sudo: sudo = "sudo "
	else: sudo = ""
	if group == None: group = __get_empty_group__()
	os.system(f"{sudo}chown {recursive}{owner}:{group} {path}")
def __delete_file_path__(path, sudo=False, forced=False):
	if sudo: sudo = "sudo "
	else: sudo = ""
	options = ""
	if forced: 
		options = " -f "
		if os.path.isdir(path): options = " -fr "
	elif os.path.isdir(path): options = " -r "
	os.system(f"{sudo}rm{options}{path}")

# converting variables.
def __array_to_string__(array, joiner=" "):
	string = ""
	for i in array:
		if string == "": string = str(i)
		else: string += joiner+str(i)
	return string
def __string_to_boolean__(string):
	if string in ["true", "True", True]: return True
	elif string in ["false", "False", False]: return False
	else: raise ValueError(f"Could not convert string [{string}] to a boolean.")
def __string_to_bash__(string):
	a = string.replace('(','\(').replace(')','\)').replace("'","\'").replace(" ","\ ").replace("$","\$").replace("!","\!").replace("?","\?").replace("@","\@").replace("$","\$").replace("%","\%").replace("^","\^").replace("&","\&").replace("*","\*").replace("'","\'").replace('"','\"')       
	return a

# generation.
def __generate_pincode__(characters=6, charset=string.digits):
	return ''.join(random.choice(charset) for x in range(characters))
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

# execute a shell script.
def __execute_script__(
	# the script in string.
	script="",
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
	path = f"/tmp/shell_script.{__generate_pincode__(characters=32)}.sh"
	__save_bytes__(path, script.encode())
	__set_file_path_permission__(path,permission=755)
	output = __execute__(
		command=[f"sh", f"{path}"],
		wait=wait,
		timeout=timeout, 
		return_format=return_format, 
		shell=shell,
		input=input,)
	__delete_file_path__(path, forced=True)
	return output

# save & load jsons.
def __load_json__(path):
	data = None
	with open(path, "r") as json_file:
		data = json.load(json_file)
	return data
def __save_json__(path, data):
	with open(path, "w") as json_file:
		json.dump(data, json_file, indent=4, ensure_ascii=False)

# save & load files.
def __load_file__(path):
	file = open(path,mode='rb')
	data = file.read().decode()
	file.close()
	return data
def __save_file__(path, data):
	file = open(path, "w+") 
	file.write(data)
	file.close()


# save & load bytes.
def __load_bytes__(path):
	data = None
	with open(path, "rb") as file:
		data = file.read()
	return data
def __save_bytes__(path, data):
	with open(path, "wb") as file:
		file.write(data)


