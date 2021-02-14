#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from syst3m.classes.config import *
from syst3m.classes import utils, console
import platform 

# kill pid.
def kill(
	# the process id.
	pid=None, 
	# root permission required.
	sudo=False,
	# loader.
	loader=True,
):
	if loader:
		log_level = 0
		loader_ = console.Loader(f"Killing process {pid}.")
	else:
		log_level = -1
	_sudo_ = Formats.Boolean(sudo).convert(true="sudo ", false="")
	output = utils.__execute_script__(f"{_sudo_}kill {pid}")
	if "terminated" in output:
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
		command = f"""{sudo}ps -ax | grep "{includes}" | """
	else:
		command = f"""{sudo}ps -ax | """
	output = utils.__execute_script__(command + """awk '{print $1"|"$2"|"$3"|"$4}' """)
	processes = {}
	for line in output.split("\n"):
		if line not in ["", " "]:
			pid,tty,_,process = line.split("|")
			processes[pid] = {
				"pid":pid,
				"tty":tty,
				"process":process,
			}
	return r3sponse.sucess_response(f"Successfully listed {len(processes)} processes.", {
		"processes":processes,
	})

# defaults object class.
class Defaults(object):
	def __init__(self):

		# variables.
		self.os = platform.system().lower()
		if self.os in ["darwin"]: self.os = "osx"
		self.home = "/home/"
		self.media = "/media/"
		self.group = "root"
		self.user = os.environ.get("USER")
		if self.os in ["osx"]:
			self.home = "/Users/"
			self.media = "/Volumes/"
			self.group = "staff"

		#
	def check_operating_system(self, supported=["osx", "linux"]):
		if self.os in ["osx"] and self.os in supported: return "osx"
		elif self.os in ["linux"] and self.os in supported: return "linux"
		else: raise ValueError(f"Unsupported operating system: [{self.os}].")
	def check_alias(self, 
		# the source name.
		alias=None, 
		# the source path.
		executable=None,
		# can use sudo.
		sudo=False,
		# overwrite.
		overwrite=False,
	):
		if sudo or cl1.argument_present("--sudo"): sudo = "sudo "
		else: sudo = ""
		l_alias = cl1.get_argument("--create-alias", required=False)
		present = "--create-alias" in sys.argv and l_alias == alias
		base = f"/usr/local/bin"
		if not os.path.exists(base):
			base = f"/usr/bin/"
		path = f"{base}/{alias}"
		if cl1.argument_present("--force") or cl1.argument_present("--forced") or overwrite or present or not os.path.exists(path):
			if l_alias != None: alias = l_alias
			#file = f"""package={executable}/\nargs=""\nfor var in "$@" ; do\n   	if [ "$args" == "" ] ; then\n   		args=$var\n   	else\n   		args=$args" "$var\n   	fi\ndone\npython3 $package $args\n"""
			file = f"""#!/usr/bin/env python3\nimport os, sys\npackage="{executable}"\nsys.argv.pop(0)\narguments = sys.argv\ns = ""\nfor i in arguments:\n	if s == "": \n		if " " in i: s = "'"+i+"'"\n		else: s = i\n	else: \n		if " " in i: s += " '"+i+"'"\n		else: s += " "+i\nos.system("python3 "+package+" "+s)"""
			os.system(f"{sudo}touch {path}")
			os.system(f"{sudo}chmod +x {path}")
			os.system(f"{sudo}chown {self.user}:{self.group} {path}")
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
	def get_source_path(self, path, back=1):
		return Formats.FilePath(path).base(back=back)
	def get_log_level(self):
		return cl1.get_argument("--log-level", required=False, empty=0)
	def pwd(self):
		pwd = utils.__execute_script__("pwd").replace("\n","")
		while True:
			if len(pwd) > 0 and pwd[0] == "/": pwd = pwd[1:]
			elif len(pwd) > 0 and pwd[len(pwd)-1] == "/": pwd = pwd[:-1]
			elif " " in pwd: pwd = pwd.replace(" ","")
			else: break
		return f"/{pwd}/"
# initialized classes.
defaults = Defaults()