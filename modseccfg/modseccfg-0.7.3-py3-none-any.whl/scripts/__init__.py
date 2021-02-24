# encoding: utf-8
# api: modseccfg
# title: log processor scripts/
# description: filter, preprocessing or reporting tools
# type: function
# category: log
# version: 0.3
# config:
#    { name: script_sep_menus, type: bool, value: 0, description: "Top-level menu categories for log processors & reporting tools." }
#
# Provide for log processing tools in scripts/ to be shown
# in menu, and either generate an text/image output window,
# or feed filtered/preprocessed file into logs.scan_log()
# Tools run locally, but get passed the sshfs-mnt log file.
#
# Scripts (can be shell, ruby, python, or whatever) should
# themselves carry a plugin comment block. Where type: can
# be one of: filter, preprocess, report, image.
# And category: defines the menu entry.
#
#    # title: mkgraph
#    # type: image
#    # category: prettify
#    # img: /tmp/output.jpeg
#
# With type:image the #img: entry can specify a filename,
# if it's not expressed in the command output already.
#
# Scripts can also declare additional parameters:
#
#    # title: grep_for_error_500
#    # type: filter
#    # category: preprocess
#    # params: %quick% -f %logfn%
#    # config: {name:quick, arg:--quick, type:bool, value:1}
#
# Scripts may expect a couple of arguments, which can be
# specified in params: as {place} $holder$ or %arg%.
# Using additional flags from config:, each having an arg:
# prefix in addition to the placeholder name:
# Whereas {logfn} is an implied/default script argument.
#
# Preferrably you'd have multiple wrapper scripts/ for each
# filter/graph tool.
#
# Now supports searching in ~/.config/modseccfg/scripts/


import os, re, subprocess, glob
import pluginconf
from modseccfg import vhosts, logs, icons
from modseccfg.utils import srvroot, conf
import PySimpleGUI as sg


# ./scripts/*
dirs = [re.sub("[^/]+$", "", __file__), conf.conf_dir+"/scripts/"]
# retain plugin meta from scripts
scripts = {}
# prepare PATH
os.environ["PATH"] = os.getenv("PATH") + ":" + ":".join(dirs)


# window or scan_log() pipe
class show:

    def __init__(self, raw_event="filename.sh", data={}, mainwindow=None, **kwargs):
        if not data.get("logfn"):
            return mainwindow.status("Requires a log selected")
        self.meta = scripts[raw_event]
        self.logfn = data["logfn"]
        self.fn = self.meta["fn"]
        self.args = self.get_args(self.meta)   # brings up arg: config dialog
        self.mainwindow = mainwindow
        
        if hasattr(self, self.meta["type"]):
            mainwindow._cursor("watch")
            getattr(self, self.meta["type"])(self.fn, self.logfn)
            mainwindow._cursor("arrow")
        else:
            return mainwindow.status("Unknown script type: " + self.meta["type"])
            
    # pipe output to log listbox
    def preprocess(self, fn, logfn):
        # almost like scan_log was designed for this use case
        print(self.mk_cmd())
        self.mainwindow.w["log"].update(
            logs.scan_log(pipe=self.run(), fn=self.logfn, force=1)
        )
    filter=preprocess  # `type:` alias

    # text report
    def report(self, *x):
        # window
        sg.theme("DarkGrey7");
        w = sg.Window(
            title="Report: " + self.meta.get("description", self.meta.get("title")),
            layout=[[sg.Multiline(k="out", text_color="white", background_color="black", size=(1196,824), font="Mono 12")]],
            size=(1200,840)
        );
        sg.theme(conf.theme)
        w.read(timeout=1)
        w.TKroot.config(cursor="watch")
        # fill from output
        try:
            for line in self.run():
                w.read(timeout=1)
                w["out"].print(line.decode("utf-8").rstrip())
        except Exception as e:
            w["out"].print(str(e), text_color="red")
        # window state managed by main event loop
        w.TKroot.config(cursor="arrow")
        self.mainwindow.win_register(w)

    # image report        
    def image(self, *x):
        # window
        w = sg.Window(
            title="Report: " + self.meta.get("description", self.meta.get("title")),
            layout=[[sg.Pane(border_width=0, relief="flat", orientation='v', pane_list=[
                sg.Column([[sg.Image(data=icons.vice, size=(1200,800), key="img")]]),
                sg.Column([[sg.Multiline(size=(1196,50), key="out")]])
            ])]],
            size=(1200,840)
        );
        w.read(timeout=1)
        # fill from output
        try:
            img_fn = self.meta.get("img")
            text = self.run().read().decode("utf-8")
            m = re.search("(/\S+\.(jpeg|png|svg))\\b", text)
            if m:
                img_fn = m.group(1)
            w["out"].print(text.rstrip())
            w["img"].update(filename=img_fn)
        except Exception as e:
            w["out"].print(str(e), text_color="red")
        # window state managed by main event loop
        self.mainwindow.win_register(w)        

    # popen cmd
    def run(self):
        return srvroot.popen(self.mk_cmd(), action="r", force_local=True)

    # show config dialog, collect -args from config: spec        
    def get_args(self, meta):
        fn = srvroot.fn(self.logfn)
        arg_conf = {
            "logfn": fn, "fn": fn, # aliases
            "accfn": re.sub("\b(access|error)\b", "access", fn),
            "errfn": re.sub("\b(access|error)\b", "error", fn),
        }
        if meta.get("config"):
            save = pluginconf.gui.window(
                arg_conf, {meta["id"]:1}, files=[], plugins={"main":meta},
                title=meta["title"],# icon=icons.crs,
                opt_label=True, size=(710,770)
            )
            if save:
                # loop over declarations, to prefix values in arg_conf
                for row in meta["config"]:
                    name = row["name"]
                    if not name in arg_conf:
                        continue
                    # bools are either present or not
                    if row["type"] == "bool":
                        arg_conf[name] = row["arg"] if arg_conf[name] else ""
                    # whereas --flags carry a value str
                    elif len(str(arg_conf[name])):
                        arg_conf[name] = row["arg"] + " " + arg_conf[name]
                    else:
                        del arg_conf[name]
        # now a dict of
        #   {"param":"--param value", "flag":"-q"}
        return arg_conf

    # substitute any {placeholders} in meta.params with conf_args{}
    def mk_cmd(self):
        cmd = [self.fn]
        args = self.meta.get("params", "{logfn}")
        args = re.sub("[\{\$\%](\w+)[\}\$\%]?", lambda m: self.args.get(m.group(1), " "), args)
        # return as list
        args = re.sub(".+/", "", self.fn) + " " + args
        return re.split("\s+", args)
            


# find scripts, extract meta
def scan_files():
    menu = {}
    ls = []
    for dir in dirs:
        try:
            ls = os.scandir(dir)
        except:
            continue
        for fn in ls:
            if not fn.is_file():
                continue
            meta = pluginconf.plugin_meta(f"{dir}/{fn.name}")
            if not meta.get("category") or not hasattr(show, meta.get("type")):
                #log.debug("scripts/__init__.scan_files.menu.invalid_type:", fn)
                continue
            scripts[meta["title"]] = meta
            c = meta.get("category").title()
                          # create and/or append
            menu[c] = menu.get(c, []) + [meta["title"]]
    return menu            

# inject into mainwindow.menu/layout
def init(menu, **kwargs):
    if not conf.get("script_sep_menus"):
        menu = menu[3][1] # submenus under ["Log", [→]]
    for group, files in scan_files().items():
        add = [group, sorted(files)]
        if conf.get("script_sep_menus"): add = [add]
        menu += add

# satisfy event lookup from mainwindow
def has(title):
    return title in scripts

