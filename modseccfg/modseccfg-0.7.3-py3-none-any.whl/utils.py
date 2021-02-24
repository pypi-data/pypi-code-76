# encoding: utf-8
# api: python
# type: function
# category: utils
# title:  Utils & Config
# description: various shortcut functions, config data, UI and remoting wrappers
# version: 0.4
# depends: pluginconf (>= 0.7.2), python:appdirs, python:pathlib
# config:
#   { name: sshfs_mount, type: str, value: "~/.config/modseccfg/mnt/", description: "Remote connection (sshfs) mount point", help: "This will be used for `modseccfg vps123:` invocations to bind the servers / root locally." }
#   { name: debug, type: bool, value: 0, description: modseccfg debug messages, help: terribly startup slowdown }
# state: alpha
# license: Apache-2.0
#
# Contains some utility code, and Python module monkeypatching.
#
# With `srvroot` all file access gets encapsulated, so it works
# locally or over sshfs.
#
# The `conf` dict is read from `~/.config/modseccfg/settings.json`.
# Defaults are built in, or module-extracted via pluginconf. The
# settings GUI also courtesy of.
#


import sys
import os
import pathlib
import re
import functools
import subprocess
import importlib
import atexit
import json
import pluginconf, pluginconf.gui
import appdirs
try: import frosch; frosch.hook()
except: pass
import logging, inspect, traceback


#-- dict mirrored into object properties
class DictObj(dict):
    def __init__(self, dict={}):
        self.__dict__ = self
        self.update(dict)

#-- config defaults
conf = DictObj({
    # mainwindow
    "theme": "DefaultNoMoreNagging",
    "switch_auto": 0,
    "keyboard_binds": 1,
    # writer
    "edit_sys_files": False,
    "backup_files": True,
    "backup_dir": "~/backup-config/",
    # logs
    "log_entries": 5000,
    "log_filter": "(?!404|429)[45]\d\d",
    "log_skip_rx" : "PetalBot|/.well-known/ignore.cgi",
    "add_stub_logs": 1,    # data/common_false_*.log
    "log_extra": "",
    "log_max_days": 3,
    "log_strip_json": 0,
    "logview_colorize": 1,
    # utils
    "sshfs_mount": "~/mnt/",
    "sshfs_o": "",
    "conf_dir": appdirs.user_config_dir("modseccfg", "io"),
    "conf_file": "settings.json",
    "plugins": {
        "__init__": 1,
        "mainwindow": 1,
        "appsettings": 1,
        "utils": 1,
        "vhosts": 1,
        "logs": 1,
        "writer": 1,
        "editor": 1,
        "ruleinfo": 1,
        "advise": 1,
        "recipe": 1,
    }
})

#-- plugin lookup
pluginconf.module_base = __name__
pluginconf.plugin_base = [__package__]
for module,meta in pluginconf.all_plugin_meta().items():
    pluginconf.add_plugin_defaults(conf, conf.plugins, meta, module)

# invoked from main
def load_plugins():
    add = []
    for name, state in conf.plugins.items():
        module_name = f"modseccfg.{name}"
        if state and not name.startswith("_") and not module_name in sys.modules:
            try:
                add.append(importlib.import_module(module_name))
            except:
                log.error(traceback.format_exc())
    return add

#-- path
def expandpath(dir):
    return str(pathlib.Path(dir).expanduser())

#-- @decorator to override module function
@functools.singledispatch
def inject(*mods):
    def decorator(func):
        for mod in mods:
            setattr(mod, func.__name__, func)
    return decorator
#-- patch re for \h support
@inject(re)
def compile(regex, *kargs, re_compile_orig=re.compile, **kwargs):
    if type(regex) is str:
        regex = re.sub(r'\\h(?![^\[]*\])', r'[\ \t\f]', regex)
        #print("re_compile: " + regex)
    return re_compile_orig(regex, *kargs, **kwargs)
@inject(re)
def grep(regex, list, flags=0):
    return [s for s in list if re.search(regex, s, flags)]
    


#-- remote/sshfs bindings
#
# This wraps any modseccfg file operations on config or log files.
# If modseccfg is started with a ssh:/ parameter, then we'll connect
# the remote file system. All file IO uses the mount prefix henceforth;
# thusly enabling remote log scans and config editing.
# (Because X11 forwarding with Python/Tkinter is unworkable at best.)
#
class remote:

    # initialize if argv[] contains any `(user@)hostname:/`
    def __init__(self, srv=[]):
        if not srv:
            self.local = 1
            self.mnt = ""
            self.srv = self.srvname = ""
        else:
            self.local = 0
            self.srvname = re.sub(":.*?$", "", srv[0])
            self.srv = self.srvname + ":/"   # must be / root
            self.mnt = expandpath(conf.sshfs_mount) + "/" + self.srv
            os.makedirs(self.mnt, 0o0700, True)
            self.mount()

    def mount(self):
        opts = []
        for opt in re.findall("(?<!-)\\b[\w=]+", conf.get("sshfs_o", "")):
            opts += ["-o", opt]
        cmd = ["sshfs"] + opts + [self.srv+"/", self.mnt]
        if self.mnt and self.srv:
            print(f"srvroot.mount = {cmd}")
            subprocess.run(cmd)
            atexit.register(self.umount)

    def umount(self):
        cmd = ["fusermount", "-u", self.mnt]
        if self.mnt and self.srv:
            print(f"srvroot.umount = {cmd}")
            subprocess.run(cmd)
            os.rmdir(self.mnt)

    def fn(self, fn):
        return self.mnt + fn

    def read(self, fn):
        if not self.exists(fn):
            if not re.search("letsencrypt|ssl", fn):
                print("WARNING: file not found", self.mnt, fn)
            return ""
        with open(self.fn(fn), "r", encoding="utf8") as f:
            return f.read()

    def write(self, fn, src):
        with open(self.fn(fn), "w", encoding="utf8") as f:
            return f.write(src)

    def popen(self, cmd, action="r", force_local=False):
        if not self.local and not force_local:
            cmd = ["ssh", self.srvname] + cmd
            print(f"srvroot.popen = {cmd}")
        if action=="r":
            return subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
        elif action=="e":
            return subprocess.Popen(cmd, stderr=subprocess.PIPE).stderr
        else:
            return subprocess.Popen(cmd, stdin=subprocess.PIPE).stdin

    def exists(self, fn):
        return os.path.exists(self.fn(fn))

    def writable(self, fn):
        if self.local:
            return os.access(self.fn(fn), os.W_OK)
        else:
            return True  # need a real test here
    writeable=writable  # alias
            
# initialize with argv[]
srvroot = remote(re.grep("\w+:", sys.argv[1:]))



#-- read config file
def cfg_read():
    fn = conf.conf_dir + "/" + conf.conf_file
    if os.path.exists(fn):
        conf.update(json.load(open(fn, "r", encoding="utf8")))

# write config file
def cfg_write():
    os.makedirs(conf.conf_dir, 0o755, True)
    #print(str(conf))
    fn = conf.conf_dir + "/" + conf.conf_file
    json.dump(conf, open(fn, "w", encoding="utf8"), indent=4)

# show config option dialog
def cfg_window(mainself, *kargs):
    fn_py = __file__.replace("utils", "*")
    init_py = fn_py.replace("*.py", "*/_*.py")
    save = pluginconf.gui.window(conf, conf.plugins, files=[fn_py, init_py], theme=conf.theme)
    if save:
        cfg_write()

# initialze conf{}
cfg_read()


# prepare logging, and log.with.module.context.warn(…) support
logging.basicConfig(level=logging.DEBUG if conf.get("debug") else logging.WARN)
class log:
    ls = []
    # fluid call collector
    def __getattr__(self, name):
        if not self.ls:
            frame = inspect.stack()[1]
            self.ls = [re.sub("^.+/|\.py$", "", str(frame.filename)), str(frame.function)+"()"]
        self.ls.append(name)
        return self
    # invoke logging.call()
    def __call__(self, *args, **kwargs):
        method = self.ls.pop()
        args = ":".join(self.ls) + ":" + ", ".join(str(a) for a in args)
        getattr(logging, method)(args)
        self.ls = []
log = log()
