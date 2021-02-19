#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from syst3m.classes.config import *
from syst3m.classes import utils, console
import platform 

# vars.
vars = r3sponse.ResponseObject({
	"os": platform.system().lower(),
	"user": os.environ.get("USER"),
	"owner": os.environ.get("USER"),
	"group": "root",
	"media": f"/media/{os.environ.get('USER')}",
	"homes": "/home/",
	"home": f"/home/{os.environ.get('USER')}/",
})
if vars.os in ["darwin"]:  
	vars.os = "macos"
	vars.group = "staff"
	vars.media = f"/Volumes/"
	vars.homes = "/Users/"
	vars.home = f"/Users/{vars.user}/"

# universal options.
options = r3sponse.ResponseObject({
	"interactive": not cl1.arguments_present(["--non-interactive"]),
	"json": cl1.arguments_present(["-j", "--json"]),
	"log_level": int(cl1.get_argument("--log-level", required=False, default=0)),
})

# get operating system.
def operating_system(supported=["*"]):
	os = vars.os
	if os in ["macos"] and ("*" in supported or os in supported): return "macos"
	elif os in ["linux"] and ("*" in supported or os in supported): return "linux"
	else: raise ValueError(f"Unsupported operating system: [{os}].")

# create alias.
def alias(
	# the source name.
	alias=None, 
	# the source path.
	executable=None,
	# can use sudo.
	sudo=False,
	# overwrite.
	overwrite=False,
):
	l_alias = cl1.get_argument("--create-alias", required=False)
	present = "--create-alias" in sys.argv and l_alias == alias
	base = f"/usr/local/bin"
	if not os.path.exists(base):
		base = f"/usr/bin/"
	path = f"{base}/{alias}"
	if ((cl1.argument_present("--force") or cl1.argument_present("--forced") or overwrite) and present) or (present or not os.path.exists(path)):
		if l_alias != None: alias = l_alias
		#file = f"""package={executable}/\nargs=""\nfor var in "$@" ; do\n   	if [ "$args" == "" ] ; then\n   		args=$var\n   	else\n   		args=$args" "$var\n   	fi\ndone\npython3 $package $args\n"""
		sudo = Formats.Boolean("--sudo" in sys.argv).convert(true="sudo ",false="")
		file = f"""#!/usr/bin/env python3\nimport os, sys\npackage="{executable}"\nsys.argv.pop(0)\narguments = sys.argv\ns = ""\nfor i in arguments:\n	if s == "": \n		if " " in i: s = "'"+i+"'"\n		else: s = i\n	else: \n		if " " in i: s += " '"+i+"'"\n		else: s += " "+i\nif os.path.exists("/usr/bin/python3"): os.system("/usr/bin/python3 "+package+" "+s)\nelse:  os.system("python3 "+package+" "+s)"""
		os.system(f"{sudo}touch {path}")
		os.system(f"{sudo}chmod +x {path}")
		os.system(f"{sudo}chown {vars.user}:{vars.group} {path}")
		try:
			Files.File(path=f"{path}", data=file).save()
		except:
			print(f"Unable to create alias $ {alias}.")
			return None
		os.system(f"chmod +x {path}")
		if '--silent' not in sys.argv:
			print(f'Successfully created alias: {alias}.')
			print(f"Check out the docs for more info $: {alias} -h")
	if present:
		quit()

# get source path.
def source_path(path, back=1):
	return Formats.FilePath(path).base(back=back)

# get log level.
def log_level(default=0):
	return int(cl1.get_argument("--log-level", required=False, default=default))

# get current working directory.
def pwd():
	return Formats.FilePath(utils.__execute_script__("pwd").replace("\n","")).clean()

# kill pids.
def kill(
	# option 1:
	# the process id.
	pid=None, 
	# option 2:
	# all processes that includes.
	includes=None,
	# root permission required.
	sudo=False,
	# loader.
	loader=True,
):
	# kill includes.
	if includes != None:
		response = processes(includes=includes, sudo=sudo)
		if not response.success: return response
		c = 0
		for pid, info in response.processes.items():
			response = self.kill(sudo=sudo, pid=pid, loader=loader)
			if not response.success: return response
			c += 1
		if c == 0:
			return r3sponse.error_response(f"No processes found.")
		elif c == 1:
			return r3sponse.success_response(f"Successfully killed {c} process.")
		else:
			return r3sponse.success_response(f"Successfully killed {c} processes.")

	# kill pid.
	else:
		if loader:
			log_level = 0
			loader_ = console.Loader(f"Killing process {pid}.")
		else:
			log_level = -1
		_sudo_ = Formats.Boolean(sudo).convert(true="sudo ", false="")
		output = utils.__execute_script__(f"{_sudo_}kill {pid}")
		if output in ["terminated",""]:
			if output in [""]:
				response = processes(includes=pid)
				if not response.success: response
				try: 
					response.processes[pid]
					if loader: loader_.stop(success=False)
					return r3sponse.error_response(f"Failed to stop process {pid}.", log_level=log_level)
				except KeyError: a=1
			if loader: loader_.stop()
			return r3sponse.success_response(f"Successfully killed process {pid}.")
		else:
			if loader: loader_.stop(success=False)
			return r3sponse.error_response(f"Failed to stop process {pid}, error: {output}", log_level=log_level)

# list all processes.
def processes(
	# root permission.
	sudo=False,
	# all processes that include a str.
	includes=None,
):
	_sudo_ = Formats.Boolean(sudo).convert(true="sudo ", false="")
	if isinstance(includes, str):
		command = f"""{_sudo_}ps -ax | grep "{includes}" | """
	else:
		command = f"""{_sudo_}ps -ax | """
	output = utils.__execute_script__(command + """awk '{print $1"|"$2"|"$3"|"$4}' """)
	processes = {}
	for line in output.split("\n"):
		if line not in ["", " "]:
			try:
				pid,tty,_,process = line.split("|")
			except ValueError: raise ValueError(f"Unable to unpack process line: [{line}], expected format: [4] seperator: [|].")
			processes[pid] = {
				"pid":pid,
				"tty":tty,
				"process":process,
			}
	return r3sponse.success_response(f"Successfully listed {len(processes)} processes.", {
		"processes":processes,
	})


#