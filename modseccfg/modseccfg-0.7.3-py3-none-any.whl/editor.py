# api: modseccfg
# type: function
# category: gui
# title: editor
# description: simple text window to edit *.conf file
# version: 0.3
# license: Apache-2.0
# config:
#    { name: editor, type: str, value: "", description: External editor to use }
#    { name: editor_font, type: list, value: "Mono,12", description: "Font,Size" }
# state: beta
#
# Just a textbox really.


import os, re
from modseccfg import utils, writer, icons
from modseccfg.utils import srvroot, conf
import PySimpleGUI as sg
from tkinter import font


class editor:
    """
    Basic editor window.
    
    If you want to use an external tool, then configure
    `editor` in the settings. Notably this should be a
    GUI tool, else will show up in the terminal and block
    the main UI.
    """

    def __init__(self, fn, readonly=False, register=None):
        self.fn = fn
        self.readonly = readonly
        self.search = self.search_pos = ""
        self.fonts = [f"{f} 12" for f in list(set(re.grep("Mono|Cons|Robo", font.families())))]
        
        # external
        if conf.get("editor"):
            return os.system(conf.editor + " " + srvroot.fn(fn) + " &")

        # internal    
        src = srvroot.read(fn)
        layout = [
            [sg.Menu([
                ["File", ["Save", "Save To", "Close"]],
                ["Edit", ["Undo", "Redo", "---", "Cut", "Copy", "Paste", "---", "Search..."]],
                ["View", ["Font", self.fonts, "Color", ["Default", "Terminal"]]],
                ["Help", ["Info"]]
            ])],
            [
                sg.Pane([
                    sg.Column([[
                        sg.Button("Save", key="save", disabled=readonly), sg.Button("Cancel", key="cancel"),
                        sg.Text("                    Search:"), sg.Input("", key="findstr", size=(15,1), enable_events=True), sg.Button("▼", key="s")
                    ]], expand_x=1)
                ], size=(500,35))
            ],
            [
                sg.Multiline(
                    default_text=src, key="src", font=conf.get("editor_font", "Consolas 11"),
                    border_width=5, autoscroll=1, focus=True, size=(175,35)
                )
            ],
            [
                sg.StatusBar(f"1:1  |  r/{'wo'[int(readonly)]}  |  {len(src)} bytes", k="status", size=(50,1))
            ]
        ]

        # prepare widgets
        self.w = sg.Window(layout=layout, size=(930,670), title=f"Edit {srvroot.srv} {fn}", resizable=1, icon=icons.icon)
        w = self.w
        w.read(timeout=1)
        w_src = w["src"]
        w_src.set_vscroll_position(0.99)
        tk_src = w_src.Widget
        tk_src.tag_config("highlight", background="orange")

        # run event loop here, or per global dispatcher
        if not register:
            while self.event(*w.read()) != "EXIT":
                pass
        else:
            register(self.w, self.event)

    # window events
    def event(self, event, data):
        w = self.w
        w_src = w["src"]
        tk_src = w_src.Widget
        
        #print(event,data)
        if event in (sg.WIN_CLOSED, "Cancel", "cancel", "Close", "Exit") or data.get("cancel"):
            w.close()
            return "EXIT"
        elif event in ["Info"]:
            sg.popup(editor.__doc__)
        elif event == "Save To":
            fn = sg.popup_get_file(
                 title="New target filename", message="Pick new targe filename. (Won't overwrite right away. You'lll have to use [Save] later.)",
                save_as=1, default_path=self.fn, default_extension=".conf"
            )
            if fn != self.fn:
                self.fn = fn
                self.readonly = 0
                self.w["status"].update(f"1:1  |  r/w  |  {fn}")
        elif not self.readonly and event in ["Save", "save"] or data.get("save"):
            srvroot.write(self.fn, data["src"])
            if event == "save":
                w.close()
                return "EXIT"
        elif event in self.fonts:
            conf.editor_font = re.findall("^([\w\-\s]+)\s(\d+)$", event)[0]
            w_src.update(font=conf.editor_font)
            utils.cfg_write()
        elif event == "Terminal":
            w_src.update(text_color='white', background_color='black')
        elif event == "Default":
            w_src.update(text_color='black', background_color='white')
        elif event == "Undo":
            tk_src.edit_undo()
        elif event == "Redo":
            tk_src.edit_redo()
        elif event == "Copy":
            w.TKroot.clipboard_clear()
            w.TKroot.clipboard_append( tk_src.get('sel.first','sel.last') )
        elif event == "Paste":
            try: tk_src.insert("insert", w.TKroot.clipboard_get())
            except: pass
        elif event == "findstr" and len(data.get("findstr")):
            tk_src.tag_remove("highlight", "1.0", "end")
            for pos in self.find_all(tk_src, data["findstr"]):
                if pos:
                    tk_src.tag_add("highlight", pos, self.incr_index(pos, len(data["findstr"])))
        elif event in ["Search", "Search...", "s"]:
            if self.search != data["findstr"]:
                self.search = data["findstr"]
                self.search_pos = "1.0"
            self.search_pos = tk_src.search(self.search, self.incr_index(self.search_pos), nocase=1)
            if self.search_pos:
                tk_src.see(self.search_pos)
                tk_src.mark_set("insert", self.search_pos)
                w_src.SetFocus()

    # search+highlight
    def find_all(self, tk, findstr, pos="1.0"):
        ls = []
        while True:
             pos = tk.search(findstr, self.incr_index(pos, 1), nocase=1)
             if pos in ls:
                 break
             else:
                 ls.append(pos)
        return ls

    # Tk text widget index
    def incr_index(self, pos, add=1):
        if not pos or not pos.find("."):
            return "end"
        y,x = pos.split(".")
        x = int(x) + add
        return f"{y}.{x}"

