import os
import getpass
from markdown import markdown as md
#import stringIO
from jedi.api import Script
from .function import load, auto_close, get_store, tab_suggest, fill_store
from autopep8 import docstring_summary, fix_code
import gi
import asyncio
gi.require_version("GtkSource", "4")
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, GLib, Gdk, Pango, WebKit2, GtkSource, Gio, GdkPixbuf, GObject
content_ = None
started = False
HANDLED = False
USRNAME = getpass.getuser()
DIREC = f"/home/{USRNAME}/.local/share"

close_buttons = []
tab_labels = []
temp_files = []

mild_sugg_s = 0
mild_sugg_e = 4
agg_sugg_e = 2


class CustomCompletionProvider(GObject.GObject, GtkSource.CompletionProvider):
    def __init__(self, *args):
        super().__init__()
        self.match = False
        self.suggest = []

    def add_proposals(self, store: list):
        self.suggest = []
        for item in store:
            self.suggest.append(GtkSource.CompletionItem(label=item, text=item, icon=None, info=None))

    def refresh_proposal(self, proposal):
        proposal = self.suggest

    def do_get_name(self):
        return   "          Suggestion          "

    def do_match(self, context):
        return self.match

    def do_populate(self, context):
        proposals = self.suggest
        if len(proposals) < 1:
            self.match = False
            return
        context.add_proposals(self, proposals, True)
        return
    
    def hide(self, *args):
        self.match = False
    def show(self, *args):
        self.match = True

def load_line(buf, linelab, *args):
    pass


def new_page(content, file=None, fc=None, fcont:tuple=None):
    global content_, started
    if not started:
        started = True
        content['notebook'].connect("page_removed", pg_removed)
    content_ = content
    notebook = content['notebook']
    if file in content['temp']['files_opened']:
        notebook.set_current_page(content['temp']['files_opened'].index(file))
        return
    close_tab = Gtk.HBox()
    close_btn = Gtk.Button()
    close_img = Gtk.Image()
    img = Gtk.Image()
    close_lab = Gtk.Label()
    scheme = GtkSource.StyleSchemeManager()
    scheme.append_search_path(f"{DIREC}/PyEdit/Data")
    scheme = scheme.get_scheme("pyedit")

    text_view = GtkSource.View()
    text_buffer = GtkSource.Buffer()
    lang = GtkSource.LanguageManager()
    mt = "python"
    if file is not None:
        try:
            data = open(file, "r").read()

            mime = Gio.content_type_guess(
                file, bytearray(data,  encoding="utf-8"))[0]
        except :
            data = None
        mime = Gio.content_type_guess(
                file)[0]

        if str(mime).find("python") != -1:
            text_buffer.set_language(lang.get_language("python3"))

        elif str(mime).lower().find("image") != -1:
            try:
                from PIL import Image
                Image.open(file)
            except Exception as e:
                return
            else:
                mt = "Image"
                img.set_from_file(file)
        else:
            mime = lang.guess_language(file, mime)
            text_buffer.set_language(mime)
            mt = mime
    else:
        text_buffer.set_language(lang.get_language("python3"))
        mt = "untitled_file"

    text_view.set_highlight_current_line(True)

    if file is None :
        pg = notebook.get_n_pages()
        close_lab.set_text(f"*untitled {pg}")
        file = f"*untitled {pg}"

    elif fc is None:
        file_s = os.access(file, os.W_OK)
        name = file.split('/')[-1]
        try:
            if mt != "Image":
                with open(file, 'r', encoding="utf-8") as f:
                    file_dat = f.read()
                    text_buffer.set_text(file_dat)
                    if file_s is False:
                        text_view.set_editable(False)
                        name += ' - [Read-only]'
                    elif file_s and content['settings']['create_b_file']:
                        try:
                            with open(f"{file}~", "w") as f:
                                f.write(file_dat)
                        except:
                            pass

        except Exception as e:
            print("An error occured", e)
            return
        close_lab.set_text(name)
    if fcont is not None:
        fn, fd = fcont
        text_buffer.set_text(fd)

    # Set up suggestion stuff
    view_completion = text_view.get_completion()
    custom_completion_provider = CustomCompletionProvider()
    view_completion.add_provider(custom_completion_provider)
    content['temp']['suggestions'].append(custom_completion_provider)

    content['temp']['mime-types'].append(mt)
    close_img.set_from_icon_name("application-exit", Gtk.IconSize.MENU)
    close_btn.set_image(close_img)
    close_btn.connect('clicked', close_tab_cb)
    text_buffer.create_mark("line", text_buffer.get_start_iter(), True)
    text_buffer.create_mark("search", text_buffer.get_start_iter(), True)
    text_buffer.create_mark("search_end", text_buffer.get_start_iter(), True)

    close_tab.pack_start(close_lab, True, True, 0)
    close_tab.pack_end(close_btn, False, True, 0)
    close_btn.set_relief(Gtk.ReliefStyle.NONE)
    close_tab.set_hexpand(True)
    text_buffer.connect("insert-text", text_inserted)
    content['notebook'].child_set_property(close_tab, 'tab-expand', True)
    content['notebook'].child_set_property(close_tab, 'tab-fill', True)
    close_tab.show_all()
    text_view.set_buffer(text_buffer)
    text_buffer.set_modified(False)
    sm = GtkSource.Map.new()
    text_buffer.set_style_scheme(scheme)
    text_buffer.create_tag("search", background="#7de497")
    if fc is not None:
        notebook.append_page(fc, close_tab)
        content["temp"]['text_views'].append(None)
        content['temp']['files_opened'].append(None)
        content['temp']['modified'].append(None)
        content['temp']['tab-label'].append(None)
        notebook.set_tab_reorderable(fc, True)
        notebook.show_all()
        notebook.set_current_page(-1)
        return
    elif mt != "Image":
        content["temp"]['text_views'].append(text_view)
        content['temp']['files_opened'].append(file)
        content['temp']['modified'].append(False)
        content['temp']['tab-label'].append(close_lab)
    elif mt == "Image":
        content['temp']['files_opened'].append(file)
        content['temp']['tab-label'].append(close_lab)
        content["temp"]['text_views'].append(None)
        content['temp']['modified'].append(None)

    font = Pango.FontDescription(content['settings']['font'])

    text_view.connect('key_press_event', indent)
    text_view.connect("key_release_event", indent2)
    text_view.connect("button_press_event", cursor)

    text_view.connect('motion-notify-event', show_doc)
    text_buffer.connect('modified-changed', on_modified)

    content["temp"]['text_buffers'].append(text_buffer)
    content['temp']['sourcemap'].append(sm)
    close_buttons.append(close_btn)
    tab_labels.append(close_lab)

    text_view.set_top_margin(10)
    text_view.set_left_margin(5)
    text_view.set_bottom_margin(20)
    text_view.modify_font(font)

    # paned.add1(_line_box)
    sc = Gtk.ScrolledWindow()
    sc.set_hexpand(True)
    sc.set_vexpand(True)
    text_view.set_show_line_numbers(True)
    sc.add(text_view)
    if mt != "Image":
        sm.set_view(text_view)
        vb = Gtk.Paned()
        vb.pack2(sm, False, True)
        vb.pack1(sc, True, True)
        vb.set_name("themed-dark")
        text_view.show_all()
        notebook.append_page(vb, close_tab)
        notebook.set_tab_reorderable(vb, True)
        line_col(text_buffer)
    else:
        sc.remove(text_view)
        sc.add(img)
        sc.set_name("sc-img-viewer")
        notebook.append_page(sc, close_tab)
        notebook.set_tab_reorderable(sc, True)

    notebook.show_all()
    notebook.set_current_page(-1)


def pg_removed(notebook, *args):
    global HANDLED
    if HANDLED:
        HANDLED = False
        return
    try:
        del tab_labels[args[-1]]
        del close_buttons[args[-1]]
    except IndexError:
        return


def close_tab_cb(button, *args):
    global HANDLED
    "For closing Tabs"
    lab = content_["close-popup"]\
        .get_children()[0]\
        .get_children()[0]\
        .get_children()[1]\
        .get_children()[0]

    for ind, btn in enumerate(close_buttons, 0):
        if btn == button:
            if content_ is not None:
                fn = content_['temp']['files_opened'][ind].split('/')[-1]
                HANDLED = True
                if content_["temp"]["mime-types"][ind] != "Image":
                    if content_['temp']['text_views'][ind].get_buffer().get_modified() == False:
                        del close_buttons[ind]
                        del tab_labels[ind]
                        content_['notebook'].remove_page(ind)
                else:
                    if content_["temp"]['mime-types'][ind] != "Image":
                        lab.set_text(
                            'Save changes to "{}" before closing'.format(fn))
                        res = content_['close-popup'].run()
                        content_['close-popup'].hide()
                        if res == 2:

                            if not os.path.isfile(content_["temp"]['files_opened'][ind]):
                                content_['file-chooser2'].run()
                                content_['file-chooser2'].hide()
                                if content_['file-chooser2'].get_filename() is not None:
                                    save_as(
                                        content_['file-chooser2'].get_filename(), ind, content_)
                                else:
                                    pass
                            else:
                                save(ind, content_)
                            del close_buttons[ind]
                            del tab_labels[ind]
                            content_['notebook'].remove_page(ind)
                        elif res == 1:
                            return
                        elif res == 0:
                            del close_buttons[ind]
                            del tab_labels[ind]
                            content_['notebook'].remove_page(ind)
                    else:
                        del close_buttons[ind]
                        del tab_labels[ind]
                        content_['notebook'].remove_page(ind)
            break


def text_inserted(buff, it, text, *args):
    ind = content_['notebook'].get_current_page()
    if content_['temp']['mime-types'][ind] == 'python':
        load(tb=buff)
    pass


async def indent_(textview, event, *args):
    global mild_sugg_s
    key = Gdk.keyval_name(event.keyval)
    buff = textview.get_buffer()
    select = buff.get_has_selection()
    ind = 0
    for in_, tb in enumerate(content_['temp']['text_buffers']):
        if tb == buff:
            ind = in_
            break
    sugg = content_['temp']['suggestions'][ind]
    ret = auto_close(key, buff, select, content_['settings'], sugg)
    ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
    if key == "space":
        sugg.hide()
    elif len(key) > 1 :
      sugg.match = False
      sugg.hide()
    return ret

def hide_sugg(*args):
    args[0].match = False
    return False

def indent2_(*args):
    textview, event = args
    global mild_sugg_s
    key = Gdk.keyval_name(event.keyval)
    if key is None:
        return
    buff = textview.get_buffer()
    store = get_store()
    ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
    style = content_['settings']['sugg-style']
    for in_, tb in enumerate(content_['temp']['text_buffers']):
        if tb == buff:
            ind = in_
            break
    sugg = content_['temp']['suggestions'][ind]
    mime = content_['temp']['mime-types'][ind]
    if mime == "python":
        if style == "none":
            return
        elif style == "mild":
            if key == "period":
                fill_store(buff)
                store = get_store()
                if store is not None and len(store) > 1:
                    sugg.add_proposals(store)
                    sugg.show()
                mild_sugg_s = 0
            elif len(key) > 1:
                mild_sugg_s = 0
            elif mild_sugg_s == mild_sugg_e:
                fill_store(buff)
                store = get_store()
                if store is not None and len(store) > 1:
                    sugg.add_proposals(store)
                    sugg.show()
                mild_sugg_s = 0
            mild_sugg_s += 1

        elif style == "aggressive":
            if key == "period":
                fill_store(buff)
                store = get_store()
                if store is not None and len(store) > 1:
                    sugg.add_proposals(store)
                    sugg.show()
                mild_sugg_s = 0
            elif len(key) > 1:
                mild_sugg_s = 0
            elif mild_sugg_s == agg_sugg_e:
                fill_store(buff)
                store = get_store()
                if store is not None and len(store) > 1:
                    sugg.add_proposals(store)
                    sugg.show()
                mild_sugg_s = 0
            mild_sugg_s += 1
        if key == "BackSpace":
            mild_sugg_s = 0
            return
                    

    if len(key) < 2:
        fill_store(buff)
        store = get_store()
        if store is not None and len(store) > 0:
            sugg.add_proposals(store)
            sugg.show()
        elif key != "period":
            sugg.hide()
    elif len(key) > 1 and key != "period":
        sugg.hide()

    if ctrl and event.keyval == Gdk.KEY_space:
        if content_['temp']['mime-types'][ind] == 'python':
            fill_store(buff)
            store = get_store()
            if store is not None and len(store) > 1:
                sugg.add_proposals(store)
                sugg.show()

    load(tb=buff)
    #print(key)


def indent2(t, e, *o):
    GLib.idle_add(indent2_, t, e )


def indent(t, e, *o):
    line_col(t.get_buffer())
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(indent_(t, e, *o))

def cursor(tv, *args):
    if args[0].button == 3:
        copy = 5
        cut = 6
        paste = 7
        tb = tv.get_buffer()
        select = tb.get_has_selection()
        for ind, i in enumerate(content_['temp']["text_views"]):
            if i == tv:
                fn = content_['temp']['files_opened'][ind]
                mime = "."+fn.split("/")[-1].split(".")[-1]
                for extc in content_['settings']['extc']:
                    if mime == extc[0]:
                        content_['menu_items_dict'][9].set_sensitive(True)
                        content_['menu_items_dict'][10].set_sensitive(True)
                        break
                    else:
                        content_['menu_items_dict'][9].set_sensitive(False)
                        content_['menu_items_dict'][10].set_sensitive(False)
                break
        if select:
            content_['menu_items_dict'][copy].set_sensitive(True)
            content_['menu_items_dict'][cut].set_sensitive(True)
        else:
            content_['menu_items_dict'][copy].set_sensitive(False)
            content_['menu_items_dict'][cut].set_sensitive(False)
        clipboard = tv.get_clipboard(Gdk.SELECTION_CLIPBOARD)
        if clipboard.wait_for_text() == "":
            content_['menu_items_dict'][paste].set_sensitive(False)
        else:
            content_['menu_items_dict'][paste].set_sensitive(True)
        content_["n-menu"].popup(None, None, None, None,
                                 args[0].button, args[0].time)
        return True


def modify(val_index, val2_index):
    temp = close_buttons[val2_index]
    close_buttons[val2_index] = close_buttons[val_index]
    close_buttons[val_index] = temp


def save(current_index, content, f=True):
    file = content['temp']['files_opened'][current_index]
    buff = content['temp']['text_buffers'][current_index]
    start_it = buff.get_start_iter()
    end_it = buff.get_end_iter()
    text = buff.get_text(start_it, end_it, True)
    content['temp']['tab-label'][current_index].set_text(file.split('/')[-1])
    content["temp"]["modified"] = content_['temp']["modified"]
    content['temp']['files_opened'][current_index] = file
    if content['settings']['format_on_save']:
        if f:
            text = fix_code(text, encoding='utf-8')
            buff.set_text(text)
    with open(file, 'w', encoding='utf-8') as f:
        f.write(text)
    content['temp']['modified'][current_index] = False
    buff.set_modified(False)
    if f:
        content['header_bar'].set_title(file.split('/')[-1]+" - PyEdit")
    set_content(content)


def save_as(file_name, current_index, content, f=True):
    file = content['temp']['files_opened'][current_index]
    buff = content['temp']['text_buffers'][current_index]
    start_it = buff.get_start_iter()
    end_it = buff.get_end_iter()
    text = buff.get_text(start_it, end_it, True)
    content['temp']['tab-label'][current_index].set_text(
        file_name.split('/')[-1])
    content['temp']['files_opened'][current_index] = file_name
    file_name = file_name.split('file://')[-1]

    if content['settings']['format_on_save']:
        text = fix_code(text, encoding='utf-8')
        if f:
            buff.set_text(text)
    if os.path.isfile(file):
        os.rename(file, file_name)
    else:
        with open(file_name, "w") as f:
            f.write(text)

    content['temp']['modified'][current_index] = False
    buff.set_modified(False)
    if f:
        content['header_bar'].set_title(file_name.split('/')[-1]+" - PyEdit")
    content['temp']['tab-label'][current_index].show_all()
    set_content(content)


def move_sugg(textview, window):
    textbuff = textview.get_buffer()
    cur = textbuff.get_insert()
    l = textbuff.get_iter_at_mark(cur)
    loc = textview.get_cursor_locations(l)[0]
    winc = textview.buffer_to_window_coords(
        Gtk.TextWindowType.TEXT, loc.x, loc.y)
    orig = textview.get_window(Gtk.TextWindowType.TEXT).get_origin()
    winc_1 = winc[1]
    if winc[1] > 500:
        winc_1 = winc[1] - window.get_size()[1] - loc.height
    window.move(orig[1]+winc[0], orig[2]+winc_1+loc.height)


mv_sec = None


async def _show_doc(tv, e, *args):
    global mv_sec
   # if mv_sec is not None:
    #    GLib.source_remove(mv_sec)
   # mv_sec = GLib.timeout_add_seconds(
    #    2, waited, tv, e.x, e.y, (e.x_root, e.y_root))


def show_doc(tv, e, *args):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_show_doc(tv, e, *args))


def _get_doc(word: str, buff, line_col: tuple):
    full_text = str(buff.get_text(
        buff.get_start_iter(), buff.get_end_iter(), True))
    sc = Script(full_text).infer(line_col[0]+1, line_col[1])
    return sc


def waited(tv, *args):
    global mv_sec, content_
    mv_sec = None
    content_['doc-win'].hide()
    if tv.is_focus():
        winc = tv.window_to_buffer_coords(
            Gtk.TextWindowType.TEXT, args[0], args[1])
        it = tv.get_iter_at_location(winc[0], winc[1])[1]
        it2 = tv.get_iter_at_location(winc[0], winc[1])[1]
        if tv.get_iter_at_location(winc[0], winc[1])[0]:
            while 1:
                if it.get_char().isalpha() or it.get_char().isdigit() or it.get_char() == "_":
                    if not it.forward_char():
                        break
                elif it.get_char().isspace():
                    break
                else:
                    if not it.forward_char():
                        break
            while 1:
                if it2.get_char().isalpha() or it2.get_char().isdigit() or it2.get_char() == "_":
                    if not it2.backward_char():
                        break
                    pass
                elif it2.get_char().isspace():
                    break
                else:
                    if not it2.backward_char():
                        break

            it.backward_char()
            it2.forward_char()
            text = tv.get_buffer().get_text(it, it2, True)
            doc = _get_doc(text, tv.get_buffer(),
                           (it.get_line(), it2.get_line_index()))
            if len(doc) != 0:
                if len(doc[0].docstring(False)) > 0:
                    print(docstring_summary(doc[0].docstring(False)))
                    text = "<head><style>body{background-color: rgb(30,30,30);color: rgb(210,210,210);}code{background-color: rgb(90,90,90);border-radius: 2px;}</style>\
                        </head>\
                        <body> \n" + md(str(doc[0].docstring(True)), extensions=["fenced_code", 'codehilite'])\
                        + "</body>".replace("\n", "<br>")
                    content_['webview'].load_html(text)
                    # print(text)
                    content_['doc-win'].move(args[2][0], args[2][1])
                    content_['doc-win'].show()
                    content_['webview'].show_all()
    return False


def on_modified(buff):
    content = content_
    ind = content['temp']['text_buffers'].index(buff)
    content['temp']['modified'][ind] = True
    line_col(buff)


def line_col(textv):
    line_lab = content_['line-lab']
    col_lab = content_['col-lab']
    lin = int(textv.get_iter_at_mark(textv.get_insert()).get_line())+1
    col = int(textv.get_iter_at_mark(textv.get_insert()).get_line_index())
    line_lab.set_text(f'line {lin}')
    col_lab.set_text(f'col {col}')


def _change_font(content: dict, font: str):
    global content_
    content_ = content
    font = Pango.FontDescription(str(font))
    for i in content['temp']['text_views']:
        i.modify_font(font)


def change_font(cont, font):
    GLib.idle_add(_change_font, cont, font)


def get_f_img(file, mod, it):
    try:
        val = str(Gio.content_type_guess(mod.get_value(it, 1), data=None)[0])
        if mod.get_value(it, 0) != "folder":
            ico = Gtk.IconTheme().get_default().choose_icon(
                Gio.content_type_get_icon(val).get_names(), 17, 0)
            if ico is not None:
                return ico.load_icon()
        else:
            return Gtk.IconTheme().get_default().load_icon("folder", 17, 0)
    except Exception as e:
        return None


def is_app(name):
    from shutil import which
    return True if which(name) != "" else False


def set_content(cont):
    global content_
    content_ = cont
