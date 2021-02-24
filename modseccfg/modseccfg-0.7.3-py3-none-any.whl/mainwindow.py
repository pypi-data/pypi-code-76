# encoding: utf-8
# api: python
# type: main
# title: main window
# description: GUI with menus, actions, rules and logs
# category: config
# version: 0.7.3
# state:   alpha
# license: Apache-2.0
# config: 
#    { name: theme, type: select, value: DefaultNoMoreNagging, select: "Default|DarkGrey|Black|BlueMono|BluePurple|BrightColors|BrownBlue|Dark|Dark2|DarkAmber|DarkBlack|DarkBlack1|DarkBlue|DarkBlue1|DarkBlue10|DarkBlue11|DarkBlue12|DarkBlue13|DarkBlue14|DarkBlue15|DarkBlue16|DarkBlue17|DarkBlue2|DarkBlue3|DarkBlue4|DarkBlue5|DarkBlue6|DarkBlue7|DarkBlue8|DarkBlue9|DarkBrown|DarkBrown1|DarkBrown2|DarkBrown3|DarkBrown4|DarkBrown5|DarkBrown6|DarkBrown7|DarkGreen|DarkGreen1|DarkGreen2|DarkGreen3|DarkGreen4|DarkGreen5|DarkGreen6|DarkGreen7|DarkGrey|DarkGrey1|DarkGrey10|DarkGrey11|DarkGrey12|DarkGrey13|DarkGrey14|DarkGrey2|DarkGrey3|DarkGrey4|DarkGrey5|DarkGrey6|DarkGrey7|DarkGrey8|DarkGrey9|DarkPurple|DarkPurple1|DarkPurple2|DarkPurple3|DarkPurple4|DarkPurple5|DarkPurple6|DarkPurple7|DarkRed|DarkRed1|DarkRed2|DarkTanBlue|DarkTeal|DarkTeal1|DarkTeal10|DarkTeal11|DarkTeal12|DarkTeal2|DarkTeal3|DarkTeal4|DarkTeal5|DarkTeal6|DarkTeal7|DarkTeal8|DarkTeal9|Default|Default1|DefaultNoMoreNagging|Green|GreenMono|GreenTan|HotDogStand|Kayak|LightBlue|LightBlue1|LightBlue2|LightBlue3|LightBlue4|LightBlue5|LightBlue6|LightBlue7|LightBrown|LightBrown1|LightBrown10|LightBrown11|LightBrown12|LightBrown13|LightBrown2|LightBrown3|LightBrown4|LightBrown5|LightBrown6|LightBrown7|LightBrown8|LightBrown9|LightGray1|LightGreen|LightGreen1|LightGreen10|LightGreen2|LightGreen3|LightGreen4|LightGreen5|LightGreen6|LightGreen7|LightGreen8|LightGreen9|LightGrey|LightGrey1|LightGrey2|LightGrey3|LightGrey4|LightGrey5|LightGrey6|LightPurple|LightTeal|LightYellow|Material1|Material2|NeutralBlue|Purple|Python|Reddit|Reds|SandyBeach|SystemDefault|SystemDefault1|SystemDefaultForReal|Tan|TanBlue|TealMono|Topanga", description: "PySimpleGUI window theme", help: "Requires a restart to take effect." }
#    { name: switch_auto, type: bool, value: 0, description: "Automatically switch to matching error.log when selecting vhost" }
#    { name: keyboard_binds, type: bool, value: 1, description: "Enable keyboard shortcuts in main window", help: "F1=info, F3/F4=editor, F5=log-viewer, F12=settings" }
# priority: core
#
# The main window binds all processing logic together. Lists
# primarily the SecRules and their states (depending on the
# selected vhost/*.conf file). Then allows to search through
# logs to find potential false positives.
#
# [Disable] and [Enable] or Recipes will update the currently
# selected vhost.conf
#



import sys, os, re, json, subprocess
from modseccfg import utils, icons, data, vhosts, logs, writer, editor, ruleinfo, recipe, modify, install, scripts
from modseccfg.utils import srvroot, conf, inject, log
import tkinter as tk, PySimpleGUI as sg, warnings

#-- init
sg.theme(conf.theme)
log.init.info("initialize modules")
vhosts.scan_all()


#-- prepare vhost/rules/logs for UI structures
class ui:

    @inject(sg.PySimpleGUI)
    def print(s):
        if not s.startswith("***"):
            __builtins__["print"](s)
    #warnings.simplefilter("ignore") would have been simpler, but PSG uses print() for some

    # make tk widget methods more accessible
    @inject(sg.Element, sg.Window)
    def __getattr__(self, name):
        if "Widget" in self.__dict__ and hasattr(self.Widget, name):
            return getattr(self.Widget, name)
        elif "TKroot" in self.__dict__ and hasattr(self.TKroot, name):
            return getattr(self.TKroot, name)
        elif name in self.__dict__:
            return self.__dict__.get(name)

    @staticmethod
    def rules(log_count={}, rulestate={}):
        rule_tree = sg.TreeData()
        hidden = [0]
        for id,r in vhosts.rules.items():
            # skip control rules
            if r.hidden:
                hidden.append(id)
                continue
            parent = ""
            if r.chained_to:
                parent = r.chained_to
                if parent in hidden:
                    continue
            # prepare treedata attributes
            state = rulestate.get(id, "🗸")  # 🗶=disabled, ⋇=modified, ⋚=wrapped, 🗸/None=enabled, formerly: -1=➗, 0=❌, 1=, undef=✅
            rule_tree.insert(
                parent=parent,
                key=id,
                text=id,
                values=[
                   state, str(id), r.msg, r.tag_primary, log_count.get(id, 0)
                ],
                icon=icons.vice #ui_data.img_vice
            )
        return rule_tree

    #-- @decorators for mainwindow
    def needs_confn(func):
        def mask(self, data):
            if not data.get("confn"):
                return self.status("Needs config filename selected")
            func(self, data)
        return mask
    def needs_vhost(func):
        def mask(self, data):
            if not vhosts.vhosts.get(data.get("confn")):
                return self.status("Needs valid vhost.conf selected")
            func(self, data)
        return mask
    def needs_id(func):
        def mask(self, data):
            if not self.id:
                return self.status("Needs a rule selected")
            func(self, data)
        return mask


#-- widget structure
menu = [
    ["File", ["Edit conf/vhost file (F4)", "---", "Settings (F12)", "SecEngine options", "CoreRuleSet options", "Rescan configs", "---", "Test", "Debug", "Help", "About", "---", "Exit"]],
    ["Rule", ["Info (F1)", "Disable", "Enable", "Modify", "<Wrap>", "Masquerade"]],
    ["Recipe"],
    ["Log", ["Advise", "Log View (F3)", "Reread log"]],
]
layout = [
    [
        sg.Column([
            # menu
            [sg.Menu(menu, key="menu")],
            # button row
            [
                sg.Button("🛈 Info", tooltip="SecRule details"),#⭐
                sg.Button("🗶 Disable", tooltip="SecRuleRemoveById"),
                sg.Button("🗸 Enable", tooltip="remove SecRuleRemove"),
                sg.Button("⋇ Modify", tooltip="SecRuleUpdateAction/Target", disabled=0),
                sg.ButtonMenu("⋚ Wrap", ["Wrap",["<FilesMatch>","<Location>","<Directory>"]], disabled=0, k="menu_wrap"),
                sg.T(" " * 18),
                sg.Button("Filter", key="filter_log", button_color=("white","gray"), font="Sans 10", tooltip="Apply filter phrase to current log"),
                sg.Combo(values=["", "injection", "500|429", "bot"], size=(20,1), key="log_filter", enable_events=True, tooltip="Regex to filter with")
            ],
            [sg.T("  "*71+"↓")],
            # comboboxes
            [sg.Text("vhost/conf", font="bold"),
             sg.Combo(key="confn", size=(50,1), values=vhosts.list_vhosts(), enable_events=True, tooltip="Which *.conf to edit"),
             sg.Text("Log"),
             sg.Combo(key="logfn", values=logs.find_logs(), size=(30,1), enable_events=True, tooltip="Error/Audit log to show"),
             ],
        ]),
        # logo
        sg.Column([ [sg.Image(data=icons.logo)] ], element_justification='r', expand_x=1),
    ],
    # tabs
    [sg.TabGroup([[
        # rule
        sg.Tab("   SecRules                                                                        ", [[
            sg.Tree(
                key="rule", data=ui.rules(), headings=["❏","RuleID","Description","Tag","Count"],
                col0_width=0, col_widths=[1,10,65,15,10], max_col_width=500,
                justification="left", show_expanded=0, num_rows=30, #expand_row=1,
                auto_size_columns=False, enable_events=False
            )
            #], expand_x=1, expand_y=1, size=(600,500))
        ], [sg.StatusBar("...", key="status", auto_size_text=1, size=(800,1))]
        ]),
        # log
        sg.Tab("  Log                                             ", [[
            sg.Pane(k="pane", border_width=0, relief="flat", orientation='v', pane_list=[
                sg.Column([[
                    sg.Listbox(values=["... 403", "... 500"], size=(980,40), key="log", enable_events=1)
                ]], size=(1900,500), k="col_log"),
                sg.Column([[
                    sg.Multiline(size=(220,5), key="logview")
                ]], size=(1900,120), k="col_logview")
            ])
        ]])
    ]], key="active_tab")],
]



#-- GUI event loop and handlers
class gui_event_handler:

    # prepare window
    def __init__(self):
        #-- hooks
        log.init.info("scan plugins")
        self.plugins = [recipe, install, scripts] + utils.load_plugins()
        #print(self.plugins)
        for mod in self.plugins:
            if hasattr(mod, "init"):
                mod.init(menu=menu, layout=layout, mainwindow=self)
        
        #-- build
        gui_event_handler.mainwindow = self
        log.init.info("build window")
        self.w = sg.Window(
            title=f"mod_security config {utils.srvroot.srv}", layout=layout, font="Sans 12",
            size=(1200,825), return_keyboard_events=conf.keyboard_binds, resizable=1, icon=icons.icon
        )
        self.tab = "secrules"
        self.status = self.w["status"].update
        self.vh = None
        self.no_edit = [949110, 980130]
        self.win_map = {}
        self.w.read(timeout=1)
        # alias functions
        self.status = self.w["status"].update
        # layout adaptions
        self._window_resized({})  # set standard sizes (from 1900*650)
        self.w["menu"].Widget.bind("<Configure>", self._window_resized) # resize event

    # we're actually listening to `pane`, then resize contained widgets when <Configure> event fired
    def _window_resized(self, e):
        #   .w["pane"].Widget
        log.pysimplegui.debug(str(type(self.w["rule"])))
        x, y = 1200, 825
        if e:
            win = self.w.TKroot
            x, y = win.winfo_width(), win.winfo_height()
        log.event.debug("_window_resized:", x,y)
        #self.w["rule"].update(num_rows=int((y-210)/20)) # needs .AddRow/.RemoveRow
        self.w["col_log"].Widget.config(width=1900, height=min(600,y-230))
        self.w["col_logview"].Widget.config(width=1900, height=150)
    
    
   # add to *win_map{} event loop
    def win_register(self, win, cb=None):
        if not cb:
            def cb(event, data):
                win.close()
        self.win_map[win] = cb
        win.read(timeout=1)

    # demultiplex PySimpleGUI events across multiple windows
    def main(self):
        self.win_register(self.w, self.event)
        while True:
            win_ls = [win for win in self.win_map.keys()]
            log.event_loop.win_ls_length.debug(len(win_ls))
            # unlink closed windows
            for win in win_ls:
                if win.TKrootDestroyed:
                    log.event.debug("destroyed", win)
                    del self.win_map[win]
            # all gone
            if len(win_ls) == 0:
                break
            # if we're just running the main window, then a normal .read() does suffice
            elif len(win_ls) == 1 and win_ls==[self.w]:
                self.event(*self.w.read())
            # poll all windows - sg.read_all_windows() doesn't quite work
            else:
                #win_ls = self.win_map.iteritems()
                for win in win_ls:
                    event, data = win.read(timeout=20)
                    if event and event != "__TIMEOUT__" and self.win_map.get(win):
                        self.win_map[win](event, data)
                    elif event == sg.WIN_CLOSED:
                        win.close()
        sys.exit()

    # mainwindow event dispatcher
    def event(self, raw_event, data):
        if not raw_event:
            return
        # prepare common properties
        data = data or {}
        event = self._case(data.get("menu") or raw_event)
        event = gui_event_handler.map.get(event, event)
        if event.startswith("menu_"): raw_event = data[event] # raw Évéńt name for MenuButtons
        self.tab = self._case(data.get("active_tab", ""))
        self.id = (data.get("rule") or [0])[0]
        self.vh = vhosts.vhosts.get( data.get("confn") )

        # dispatch
        if event and hasattr(self, event):
            self.status("")
            getattr(self, event)(data)
            return
        elif event == "exit":
            self.w.close()
        # plugins
        mod = self._plugin_has(raw_event)
        if mod:
            mod.show(name=event, raw_event=raw_event, data=data, mainwindow=self, main=self)
        else:
            self.status(f"UNKNOWN EVENT: {event} / {data}")

    # find first plugin which has `has` and claims responsibility for raw_event (mixed-case menu entries)
    def _plugin_has(self, raw_event):
        for mod in self.plugins:
            if hasattr(mod, "has") and mod.has(raw_event):
                return mod

    # alias/keyboard map
    map = {
        sg.WIN_CLOSED: "exit",
        "none": "exit",  # happens when mainwindow still in destruction process
        "f3_69": "log_view",
        "f4_70": "edit_conf_vhost_file",
        "f5_71": "log_view",
        "f12_96": "settings",
        "return_36": "info",
        "log_filter": "filter_log",  # alias (respond to dropdown and key alike)
        "menu_modify": "modify",
    }
    
    # change in vhost combobox
    def confn(self, data):
        # switch logfn + automatically scan new error.log?
        if conf.switch_auto:
            logfn = data.get("logfn")
            logs = re.grep("error", self.vh.logs)
            if len(logs):
                self.w["logfn"].update(value=logs[0])
                self.logfn(data=dict(logfn=logs[0]))
        self._update_rules()
        self.status(self.vh.warn or f"<{self.vh.name or self.vh.t}>")

    # scan/update log
    def logfn(self, data, force=0):
        self._cursor("watch")
        self.w["log"].update(
            logs.scan_log(data["logfn"], force=force)
        )
        self._update_rules()
        self._cursor("arrow")

    # add "SecRuleRemoveById {id}" in vhost.conf
    @ui.needs_id
    @ui.needs_confn
    def disable(self, data):
        if self.id in self.no_edit and self._cancel("This rule should not be disabled (it's a heuristic/collective marker). Continue?"):
            return
        if data["confn"] and self.id:
            # Clean up comment a little (comments aren't strictly speaking allowed,
            # but mod_security effectively proccesses them and simply ignores any
            # trailing garbage. So we just need to ensure there aren't any extra
            # integers to be interpreted as RemoveById rule numbers.
            comment = re.sub("[^\w\s,:./]", "", vhosts.rules[self.id].msg)  # retain just a bit of text
            comment = re.sub("(\d)", lambda m: chr(0xFEE0 + ord(m.group(1))), comment) # integers to unicode glyphs
            writer.append(data["confn"], directive="SecRuleRemoveById", value=self.id, comment=" # "+comment)
            self._update_rulestate(self.id, "🗶")

    # remove any "SecRuleRemove* {id}" in vhost.conf
    @ui.needs_id
    @ui.needs_confn
    def enable(self, data):
        if self.vh and self.vh.rulestate.get(self.id) != "🗶" and self._cancel("SecRule might be wrapped/masked. Reenable anyway?"):
            return
        writer.remove_remove(data["confn"], "SecRuleRemoveById", self.id)
        self._update_rulestate(self.id, None)

    # File: Settings - remapped to pluginconf window
    def settings(self, data):
        utils.cfg_window(self)

    # File: Editor
    @ui.needs_confn
    def edit_conf_vhost_file(self, data):
        editor.editor(data.get("confn"), register=self.win_register)

    # `log` listbox selection change: transfer entry to `logview` textbox
    def log(self, data):
        if not data.get("log"): # empty / no selection
            return self.status("No log entry selected")
        if conf.logview_colorize:
            logs.colorize(self.w["logview"], data["log"][0])
        else:
            self.w["logview"].update(value=data["log"][0])

    # Log: Log View (F3) → readonly editor
    def log_view(self, data):
        editor.editor(data.get("logfn"), readonly=1)

    # [Info]
    @ui.needs_id
    def info(self, data):
        if self.tab == "secrules":
            self.win_register(
                *ruleinfo.show(self.id, log_values=self.w["log"].get_list_values, vh=self.vh)
            )
        else:
            print("No info() for "+self.tab) # was meant for a dialog to visualize JSON audit logs

    # [Modify]
    @ui.needs_id
    @ui.needs_confn
    def modify(self, data):
        modify.show(self.id, self, data)

    # File: SecEngine Options
    @ui.needs_confn
    def secengine_options(self, data):
        import modseccfg.secoptions
        modseccfg.secoptions.window(data.get("confn", "/etc/modsecurity/modsecurity.conf"))

    # File: CoreRuleSet options
    @ui.needs_confn
    def coreruleset_options(self, data):
        import modseccfg.crsoptions
        modseccfg.crsoptions.window(data.get("confn", "/etc/modsecuritye/crs/crs-setup.conf"))

    # File: Rescan configs
    def rescan_configs(self, data):
        self._cursor("watch")
        self.status("Strap in..")
        vhosts.vhosts = {}
        vhosts.rules = {}
        vhosts.scan_all()
        self.w["confn"].update(values=vhosts.list_vhosts())
        self.w["logfn"].update(values=logs.find_logs())
        self._cursor("arrow")
        self.status(f"{len(vhosts.vhosts)} conf files, {len(vhosts.rules)} rules")

    # Log: advise        
    def advise(self, data):
        import modseccfg.advise
        modseccfg.advise.show(self, data)

    # Log: Reread log
    def reread_log(self, data):
        self.logfn(data, force=1)
    
    # Log: Filter
    def filter_log(self, data):
        rx = data["log_filter"]
        if not rx:
            if logs.state.prev:
                self.w["log"].update(logs.state.prev)
                logs.state.prev = []
            return
        if not logs.state.prev:
            logs.state.prev = self.w["log"].get_list_values()
        rx = re.compile(rx, re.I)
        self.w["log"].update(
            values = re.grep(rx, logs.state.prev)
        )

    # File: About
    def about(self, data):
        m = utils.pluginconf.plugin_meta(module="__init__")
        sg.popup(f"{m['title']} {m['version']}\n{m['description']}\n\n{m['doc']}\n")
    # File: Help
    def help(self, uu):
        os.system(f"yelp '{data.dir}/help/index.page' &")

    # File: Debug
    def debug(self, data):
        sg.show_debugger_window()  # we need the window handle for the event loop
        w = sys.modules["PySimpleGUI.PySimpleGUI"]._Debugger.debugger.watcher_window
        self.win_register(w, lambda *x: None)

    # renew display of ruletree with current log and vhost rulestate
    def _update_rules(self, *data):
        if self.vh:
            self.w["rule"].update(ui.rules(log_count=logs.log_count, rulestate=self.vh.rulestate))

    # called from disable/enable to set 🗶=disabled, ⋇=modified, ⋚=wrapped, 🗸/None=enabled, etc
    def _update_rulestate(self, id, val):
        if self.vh:
            if val==None and id in self.vh.rulestate:
                del self.vh.rulestate[id]
            else:
                self.vh.rulestate[id] = val
            self._update_rules()

    # remove non-alphanumeric characters (for event buttons / tab titles / etc.)
    def _case(self, s):
        return re.sub("\(?\w+\)|\W+|_0x\w+$", "_", str(s)).strip("_").lower()

    # set mouse pointer ("watch" for planned hangups)
    def _cursor(self, s="arrow"):
        self.w.config(cursor=s)
        self.w.read(timeout=1)
    
    def _cancel(self, text):
        return sg.popup_yes_no(text) == "No"
        
    # tmp/dev
    def test(self, data):
        log.error("No test code")

            

#-- main
def main():
    gui_event_handler().main()


