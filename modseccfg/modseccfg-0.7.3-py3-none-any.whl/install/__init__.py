# api: modseccfg
# encoding: utf-8
# title: Install packages
# descriptions: addon packages
# version: 0.2
# type: handler
# category: setup
#
# Mirrors files from install/ dir into File→Install menu.
# Allows to install packages (locally or onto srvroot).
#

import os, sys, re, glob, subprocess, traceback
from modseccfg import writer
from modseccfg.utils import srvroot, conf
import PySimpleGUI as sg

dir = re.sub("[^/]+$", "", __file__)


# hook: mainwindow.add_menu
def init(menu, **kwargs):
    m = menu[0][1] # File
    i = 5 # m.index("Test")
    m.insert(i, ls())
    m.insert(i, "Install")
    
# find files
def ls():
    ls = [re.sub("^.+/", "", fn) for fn in glob.glob(f"{dir}/*.*")]
    ls = [fn for fn in ls if not fn.startswith("_")]
    return ls

# File→Install check
def has(event):
    return event in ls()

# actual invocation
def show(raw_event=None, mainwindow=None, **kwargs):

    cmd = raw_event
    # install command types
    if re.search("\.deb$", cmd):
        cmd = f"dpkg -i ./{cmd}"
    elif re.search("\.rpm$", cmd):
        cmd = f"rpm -i ./{cmd}"
    elif re.search("\.py$", cmd):
        cmd = f"import modseccfg.install.{cmd[0:-3]}"
    elif os.access(f"{dir}/{cmd}", os.X_OK):
        cmd = f"./{cmd}"
    # local / remote
    if cmd.startswith("import "):
        pass
    elif re.search(".local", cmd):
        cmd = open(f"{dir}/{cmd}", "r", encoding="utf-8").read()
    elif srvroot.srv:
        cmd = re.sub('\./', '/root/', cmd)
        cmd = f"scp  ./{cmd}  {srvroot.srv}root/\nssh {srvroot.srvname}  {cmd}"
        
    layout = [
       [sg.Multiline(cmd, size=(100,22), background_color="#331111", text_color="white", font=("Monospace", 13), key="cmd")],
       [sg.Button("Exec", key="Exec"), sg.Button("Close")]
    ]
    execwin(
        sg.Window(layout=layout, title="install"),
        mainwindow
    )

# event handler    
class execwin:
    def __init__(self, w, mainwindow):
        self.w = w
        self.cmd = w["cmd"]
        w.read(timeout=1)
        self.w["cmd"].Widget.config(insertbackground="yellow")
        mainwindow.win_register(w, self.event)

    def event(self, event, data):
        if event=="Exec":
            self.w["Exec"].update(disabled=1, visible=0)
            self.run(data["cmd"])
        elif event=="Close":
            self.w.close()

    # iterate over cmd lines, and run each
    def run(self, cmds):
        os.chdir(dir)
        self.cmd.update("")
        #print(cmds)
        if re.match("import [\w\.]+", cmds):
            self.include(cmds)
            cmds = ""
        for line in cmds.split("\n"):
            if not re.match("^\s*[\w.]", line):
                self.cmd.print(line, text_color="gray")
                continue
            self.cmd.print(f"> {line}\n", text_color="lightgreen")
            args = re.split("\s+", line)
            try:
                r = subprocess.run(args, capture_output=True)
            except Exception as e:
                self.cmd.print(str(e), text_color="red", background_color="#553311")
                break
            if r.stdout:
                self.cmd.print(str(r.stdout.decode("utf-8")))
            if r.returncode:
                self.cmd.print(f"ERRNO {r.returncode}", background_color="yellow", text_color="red", end="")
                self.cmd.print("")
            if r.stderr:
                self.cmd.print(str(r.stderr.decode("utf-8")), text_color="red")
                self.cmd.print("")
            if r.returncode:
                break
        #sg.popup("Completed?")
        #self.w.read(timeout=15000)
        #self.w.close()

    # __import__ .py file
    def include(self, cmd):
        self.cmd.reroute_stdout_to_here()
        self.cmd.print(cmd, text_color="green")
        import importlib
        fn = re.findall("import (\w+(?:\.\w+)+)", cmd)[0]
        try:
            importlib.import_module(fn)
            del sys.modules[fn]
        except Exception as e:
            self.cmd.print(str(e), text_color="red")
        self.cmd.restore_stdout()
    