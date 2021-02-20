# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.messagebox
import sys
from tkinter import ttk
import traceback
from tkinter import filedialog

from quick_data_clean.quick_common import Common
from quick_data_clean.quick_common import except_decorator

import windnd
from types import FunctionType, MethodType


class Widget(object):

    is_frist_menu = True
    menubar = None
    user_info = ""
    copyfie_info = ""

    def except_decorator_before_run_win(func):
        def make_decorater(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                traceback.print_exc(file=open(Common.err_log_file_name, "w"))

                error_str = ""
                with open(Common.err_log_file_name, "r") as f:
                    while True:
                        buf_str = f.readline()
                        if buf_str:
                            error_str += buf_str
                        else:
                            break

                if "if_main_win_run" in dir(args[0]):
                    if not args[0].if_main_win_run:
                        if args[0].main_win_obj:
                            args[0].main_win_obj.withdraw()
                        else:
                            tkinter.Tk().withdraw()
                else:
                    tkinter.Tk().withdraw()

                raise

        return make_decorater

    @except_decorator_before_run_win
    def increase_y_pos_label(self):
        self.controll_x = 10
        self.controll_y = self.controll_y + 25

    @except_decorator_before_run_win
    def add_label(self, label_text):

        Common.check_assign_type(label_text, Common.type_string,
                                 "the first parameter of add_label_text")

        tk.Label(self.main_win_obj,
                 text=label_text).place(x=self.controll_x,
                                        y=self.controll_y)

        self.increase_y_pos_label()

    @except_decorator_before_run_win
    def add_menu_list(self, menu_title, menu_item, command_item):

        if self.is_frist_menu:
            self.menubar = tk.Menu(self.main_win_obj)
            self.is_frist_menu = False

        current_menu = tk.Menu(self.main_win_obj)
        for index, item in enumerate(menu_item):
            current_menu.add_command(label=item,
                                     command=command_item[index])

        self.menubar.add_cascade(label=menu_title, menu=current_menu)

        self.main_win_obj['menu'] = self.menubar

    @except_decorator_before_run_win
    def show_user_info(self):
        self.messagebox(self.user_info, "使用说明")

    @except_decorator_before_run_win
    def show_copyright_info(self):
        self.messagebox(self.copyfie_info, "版权信息")

    @except_decorator_before_run_win
    def add_about_menu(self, user_info,
                       copyfie_info="All right reserved (C) 2019 Jaymi"):

        self.user_info = user_info
        self.copyfie_info = copyfie_info

        if self.is_frist_menu:
            self.menubar = tk.Menu(self.main_win_obj)
            self.is_frist_menu = False

        menu_item = ["使用说明", "版权信息"]
        command_item = [self.show_user_info, self.show_copyright_info]

        current_menu = tk.Menu(self.main_win_obj)
        for index, item in enumerate(menu_item):
            current_menu.add_command(label=item,
                                     command=command_item[index])

        self.menubar.add_cascade(label="关于", menu=current_menu)

        self.main_win_obj['menu'] = self.menubar

    @except_decorator_before_run_win
    def create_main_win(self, title, hight=400):

        self.main_win_obj = tk.Tk()

        self.main_win_obj.title(title)

        self.if_main_win_run = False

        self.hight = hight

        self.width = 600

        self.row = 0

        self.button_height = 2

        self.button_width = 20

        self.controll_y = 10

        self.controll_x = 10

        self.encry_var_dict = {}

        self.combox_var_dict = {}

        self.checkbox_var_dict = {}

        self.progressbar_var_dict = {}

        self.progressbar_dict = {}

        self.if_main_win_run = False

        self.progressbar_mode_increaing = 0

        self.progressbar_mode_repeat = 1

        self.text_drop_dict = {}

        self.text_count = 0

    @except_decorator_before_run_win
    def run_main_win(self):

        self.center_window(self.width, self.hight)

        self.main_win_obj.maxsize(self.width, self.hight * 2)

        self.main_win_obj.minsize(self.width, self.hight)
        self.if_main_win_run = True
        self.main_win_obj.mainloop()

    @except_decorator_before_run_win
    def destroy_main_win(self):
        self.main_win_obj.destroy()

    def __hide_main_win_if_not_run(self):
        if self.main_win_obj:
            self.main_win_obj.withdraw()

    @except_decorator_before_run_win
    def hide_main_win_for_messagbox(self):
        if "if_main_win_run" in dir(self):
            if not self.if_main_win_run:
                if self.main_win_obj:
                    self.main_win_obj.withdraw()
                else:
                    tkinter.Tk().withdraw()
        else:
            tkinter.Tk().withdraw()

    @except_decorator_before_run_win
    def hide_main_win(self):
        if self.main_win_obj:
            self.main_win_obj.withdraw()

    @except_decorator_before_run_win
    def show_main_win(self):
        if self.main_win_obj:
            self.main_win_obj.update()
            self.main_win_obj.deiconify().withdraw()

    def get_screen_size(self):
        return self.main_win_obj.winfo_screenwidth(),
        self.main_win_obj.winfo_screenheight()

    def get_window_size(self):
        return self.main_win_obj.winfo_reqwidth(),
        self.main_win_obj.winfo_reqheight()

    def center_window(self, width, height):
        screenwidth = self.main_win_obj.winfo_screenwidth()
        screenheight = self.main_win_obj.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height,
                                (screenwidth - width) / 2,
                                (screenheight - height) / 2)
        self.main_win_obj.geometry(size)

    def __add_label_text_old(self, hold_text, button_name,
                             button_width=20, button_height=1):

        tk.Entry(self.main_win_obj,
                 show=None,
                 font=('Arial', 14)).grid(row=self.row,
                                          column=1,
                                          padx=10,
                                          pady=10,
                                          ipadx=10,
                                          ipady=10,
                                          sticky=tk.N)
        tk.Button(self.main_win_obj, text=button_name,
                  width=button_width,
                  height=button_height,
                  command=hit_me).grid(row=self.row,
                                       column=0,
                                       padx=10,
                                       pady=10, ipadx=10, ipady=10)

        self.row = self.row + 1

    def __add_lable_button_old(self, label_name, button_name,
                               button_width=20):

        tk.Label(self.main_win_obj, text=label_name, width=30, height=2).grid(
            row=self.row,
            column=0, padx=10, pady=10, ipadx=10, ipady=10)

        tk.Button(
            self.main_win_obj,
            text=button_name,
            width=button_width,
            height=self.button_height,
            command=hit_me).grid(row=self.row, column=1,
                                 padx=10, pady=10, ipadx=10, ipady=10)

        self.row = self.row + 1

    @except_decorator_before_run_win
    def increase_y_pos(self):
        self.controll_x = 10
        self.controll_y = self.controll_y + 60

    @except_decorator_before_run_win
    def add_text_button(self, text_id_name, button_name, command_func):

        self.create_text(text_id_name, self.controll_x,
                         self.controll_y, 410, 48)

        tk.Button(
            self.main_win_obj,
            text=button_name,
            width=self.button_width,
            height=self.button_height,
            command=command_func).place(x=self.width - self.button_width - 150,
                                        y=self.controll_y, anchor=tk.NW)
        self.increase_y_pos()

    @except_decorator_before_run_win
    def add_label_text(self, label_text, text_id_name):

        Common.check_assign_type(label_text, Common.type_string,
                                 "the first parameter of add_label_text")

        Common.check_assign_type(text_id_name, Common.type_string,
                                 "the second parameter of add_label_text")

        tk.Label(self.main_win_obj,
                 text=label_text).place(x=self.controll_x,
                                        y=self.controll_y,
                                        width=130,
                                        height=48)

        self.create_text(text_id_name,
                         self.controll_x + 140, self.controll_y, 430, 48)

        self.increase_y_pos()

    @except_decorator_before_run_win
    def add_button(self, button_name, command_func):

        Common.check_assign_type(button_name, Common.type_string,
                                 "the first parameter of add_button")

        Common.check_assign_type(command_func, Common.type_function,
                                 "the second parameter of add_button")

        tk.Button(
            self.main_win_obj,
            text=button_name,
            width=self.button_width,
            height=self.button_height,
            command=command_func).place(x=self.width - self.button_width - 150,
                                        y=self.controll_y, anchor=tk.NW)

        self.increase_y_pos()

    def dragged_files_conf(self, te1, text_id_name):

        if self.text_count > 10:
            return

        func_name = 'dragged_files_{}'.format(text_id_name)
        self.text_drop_dict[func_name] = text_id_name

        func_code = 'def dragged_files_{}(self, files): import sys;func_name=sys._getframe().f_code.co_name;self.set_text(self.text_drop_dict[func_name], files[0].decode("gbk"))'.format(text_id_name)
        func_code_c = compile(func_code, "<string>", "exec")
        dragged_func = FunctionType(func_code_c.co_consts[0],
                                    globals(),
                                    func_name)

        if self.text_count == 1:
            self.dragged_filesfunc_name1 = MethodType(dragged_func, self)
            windnd.hook_dropfiles(te1, func=self.dragged_filesfunc_name1)
        elif self.text_count == 2:
            self.dragged_filesfunc_name2 = MethodType(dragged_func, self)
            windnd.hook_dropfiles(te1, func=self.dragged_filesfunc_name2)
        elif self.text_count == 3:
            self.dragged_filesfunc_name3 = MethodType(dragged_func, self)
            windnd.hook_dropfiles(te1, func=self.dragged_filesfunc_name3)
        elif self.text_count == 4:
            self.dragged_filesfunc_name4 = MethodType(dragged_func, self)
            windnd.hook_dropfiles(te1, func=self.dragged_filesfunc_name4)
        elif self.text_count == 5:
            self.dragged_filesfunc_name5 = MethodType(dragged_func, self)
            windnd.hook_dropfiles(te1, func=self.dragged_filesfunc_name5)
        elif self.text_count == 6:
            self.dragged_filesfunc_name6 = MethodType(dragged_func, self)
            windnd.hook_dropfiles(te1, func=self.dragged_filesfunc_name6)
        elif self.text_count == 7:
            self.dragged_filesfunc_name7 = MethodType(dragged_func, self)
            windnd.hook_dropfiles(te1, func=self.dragged_filesfunc_name7)
        elif self.text_count == 8:
            self.dragged_filesfunc_name8 = MethodType(dragged_func, self)
            windnd.hook_dropfiles(te1, func=self.dragged_filesfunc_name8)
        elif self.text_count == 9:
            self.dragged_filesfunc_name9 = MethodType(dragged_func, self)
            windnd.hook_dropfiles(te1, func=self.dragged_filesfunc_name8)
        elif self.text_count == 10:
            self.dragged_filesfunc_name10 = MethodType(dragged_func, self)
            windnd.hook_dropfiles(te1, func=self.dragged_filesfunc_name10)

    def create_text(self, text_id_name, x_, y_, width_, height_):
        self.is_id_exist(text_id_name)
        var = tk.StringVar()
        te1 = tk.Entry(self.main_win_obj,
                       show=None,
                       textvariable=var,)
        te1.place(x=x_, y=y_, width=width_, height=height_, anchor=tk.NW)

        self.encry_var_dict[text_id_name] = var

        self.text_count += 1

        self.current_text_id = text_id_name

        self.dragged_files_conf(te1, text_id_name)

    @except_decorator_before_run_win
    def add_text(self, text_id_name):

        Common.check_assign_type(text_id_name, Common.type_string,
                                 "the first parameter of add_text")

        self.create_text(text_id_name, self.controll_x, self.controll_y,
                         570, 48)

        self.increase_y_pos()

    def get_debug_info(self):
        return "File: {0} Func: {1} Line: {2}".format(
            sys._getframe().f_code.co_filename,
            sys._getframe().f_code.co_name,
            sys._getframe().f_lineno)

    def is_id_exist(self, text_id_name):
        if text_id_name == "":
            raise Exception("text_id_name cannot be a empty string.")

        if text_id_name in self.encry_var_dict:
            raise Exception("text_id_name: {0} already exist. ".format(
                text_id_name))

    def get_text(self, text_id_name):
        self.check_id(text_id_name, self.encry_var_dict)
        return self.encry_var_dict[text_id_name].get()

    def set_text(self, text_id_name, data):
        self.check_id(text_id_name, self.encry_var_dict)
        self.encry_var_dict[text_id_name].set(data)

    def is_comboxid_exist(self, comboxlist_id_name):
        if comboxlist_id_name == "":
            raise Exception("comboxlist_id_name cannot be a "
                            "empty string.")

        if comboxlist_id_name in self.combox_var_dict:
            raise Exception("comboxlist_id_name: {0} "
                            "already exist.".format(comboxlist_id_name))

    def create_comboxlist(self, comboxlist_id_name, item,
                          x_, y_, width_, height_,
                          select_change_command_func=None,
                          select_item=0):

        self.is_comboxid_exist(comboxlist_id_name)

        com_var = tk.StringVar()
        comboxlist = ttk.Combobox(self.main_win_obj, textvariable=com_var)
        comboxlist["values"] = item
        comboxlist.current(select_item)
        comboxlist.bind("<<ComboboxSelected>>", select_change_command_func)
        comboxlist.place(
            x=x_,
            y=y_,
            width=width_,
            height=height_,
            anchor=tk.NW)

        self.combox_var_dict[comboxlist_id_name] = com_var

    @except_decorator_before_run_win
    def add_label_comboxlist(self, label_text, comboxlist_id_name, item,
                             select_change_command_func=None,
                             select_item=0):

        Common.check_assign_type(label_text, Common.type_string,
                                 "the first parameter of add_label_comboxlist")

        Common.check_assign_type(comboxlist_id_name, Common.type_string,
                                 "the second parameter of "
                                 "add_label_comboxlist")

        Common.check_assign_type(item, Common.type_list,
                                 "the third parameter of "
                                 "add_label_comboxlist")

        if select_change_command_func:
            Common.check_assign_type(select_change_command_func,
                                     Common.type_function,
                                     "the fourth parameter of "
                                     "add_label_comboxlist")

        Common.check_assign_type(select_item, Common.type_int,
                                 "the fifth parameter of "
                                 "add_label_comboxlist")

        tk.Label(self.main_win_obj,
                 text=label_text).place(x=self.controll_x,
                                        y=self.controll_y,
                                        width=130,
                                        height=48)

        self.create_comboxlist(comboxlist_id_name, item,
                               self.controll_x + 160,
                               self.controll_y,
                               410,
                               48,
                               select_change_command_func,
                               select_item)

        self.increase_y_pos()

    @except_decorator_before_run_win
    def add_comboxlist(self, comboxlist_id_name, item,
                       select_change_command_func=None,
                       select_item=0):

        Common.check_assign_type(comboxlist_id_name, Common.type_string,
                                 "the first parameter of add_comboxlist")

        Common.check_assign_type(item, Common.type_list,
                                 "the second parameter of add_comboxlist")

        if select_change_command_func:
            Common.check_assign_type(select_change_command_func,
                                     Common.type_function,
                                     "the third parameter of add_comboxlist")

        Common.check_assign_type(select_item, Common.type_int,
                                 "the fourth parameter of add_comboxlist")

        self.create_comboxlist(comboxlist_id_name, item,
                               self.controll_x,
                               self.controll_y,
                               570,
                               48,
                               select_change_command_func,
                               select_item)

        self.increase_y_pos()

    def get_comboxlist(self, comboxlist_id_name, index=0):
        return self.combox_var_dict[comboxlist_id_name].get()

    def __set_comboxlist(self, comboxlist_id_name, index):
        self.combox_var_dict[comboxlist_id_name].current(index)

    def is_checkboxid_exist(self, checkbox_id_name):
        if checkbox_id_name == "":
            raise Exception("checkbox_id_name cannot be a "
                            "empty string.")

        if checkbox_id_name in self.checkbox_var_dict:
            raise Exception("checkbox_id_name: {0} "
                            "already exist.".format(checkbox_id_name))

    def create_checkbox(self, text_, checkbox_id_name,
                        x_, y_):
        var1 = tk.BooleanVar()

        self.is_checkboxid_exist(checkbox_id_name)

        tk.Checkbutton(self.main_win_obj, text=text_,
                       variable=var1,
                       onvalue=True,
                       offvalue=False).place(x=x_,
                                             y=y_,
                                             anchor=tk.NW)
        self.checkbox_var_dict[checkbox_id_name] = var1

    @except_decorator_before_run_win
    def add_checkbox(self, checkbox_info):

        Common.check_assign_type(checkbox_info, Common.type_list,
                                 "the first parameter of add_checkbox")

        if len(checkbox_info) == 0:
            raise Exception("checkbox_info cannot be a empty list.")

        if len(checkbox_info) > 4:
            raise Exception("size of checkbox_info cannot be "
                            "Greater than 4.")

        for info in checkbox_info:
            checkbox_text = info[0]
            checkbox_id_name = info[1]

            if len(checkbox_text) == 0:
                raise Exception("checkbox_text cannot be a empty "
                                "string.")

            self.create_checkbox(checkbox_text, checkbox_id_name,
                                 self.controll_x, self.controll_y)

            self.controll_x = self.controll_x + 150

        self.increase_y_pos()

    def get_checkbox(self, checkbox_id_name):
        return self.checkbox_var_dict[checkbox_id_name].get()

    def check_id(self, id_name, dict_obj):
        if id_name not in dict_obj:
            raise Exception("id_name: {0} "
                            "not exist.".format(id_name))

    def is_progressbarid_exist(self, progressbar_id_name):
        if progressbar_id_name == "":
            raise Exception("progressbar_id_name cannot be a "
                            "empty string.")

        if progressbar_id_name in self.progressbar_var_dict:
            raise Exception("progressbar_id_name: {0} "
                            "already exist.".format(progressbar_id_name))

    def create_progressbar(self, progressbar_id_name,
                           max_value,
                           current_value,
                           width_,
                           x_,
                           y_,
                           mode_):
        self.is_progressbarid_exist(progressbar_id_name)
        mode_srr = ""
        if mode_ == self.progressbar_mode_repeat:
            mode_srr = "indeterminate"
        else:
            mode_srr = "determinate"
        var = tk.IntVar()
        progress = ttk.Progressbar(self.main_win_obj,
                                   orient="horizontal",
                                   length=300,
                                   variable=var,
                                   mode=mode_srr)
        progress["maximum"] = max_value
        progress["value"] = current_value
        var.set(current_value)
        progress.place(x=x_, y=y_,
                       width=width_, height=48, anchor=tk.NW)

        self.progressbar_var_dict[progressbar_id_name] = var
        self.progressbar_dict[progressbar_id_name] = progress

    @except_decorator_before_run_win
    def add_progressbar(self, progressbar_id_name,
                        max_value=100,
                        current_value=0,
                        mode_=0):

        self.create_progressbar(progressbar_id_name,
                                max_value,
                                current_value,
                                570,
                                self.controll_x,
                                self.controll_y,
                                mode_)

        self.increase_y_pos()

    @except_decorator_before_run_win
    def add_label_progressbar(self, label_text, progressbar_id_name,
                              max_value=100,
                              current_value=0,
                              mode_=0):

        tk.Label(self.main_win_obj,
                 text=label_text).place(x=self.controll_x,
                                        y=self.controll_y,
                                        width=130,
                                        height=48)

        self.create_progressbar(progressbar_id_name,
                                max_value,
                                current_value,
                                430,
                                self.controll_x + 140,
                                self.controll_y,
                                mode_)

        self.increase_y_pos()

    def get_progressbar(self, progressbar_id_name):
        return self.progressbar_var_dict[progressbar_id_name].get()

    def set_progressbar(self, progressbar_id_name, value):
        self.progressbar_var_dict[progressbar_id_name].set(value)
        self.main_win_obj.update()

    def set_progressbar_max_value(self, progressbar_id_name, value):
        self.progressbar_dict[progressbar_id_name]["maximum"] = value

    def get_value_from_simpledialog(self, dlg_title, dlg_info, value_type):

        from tkinter import simpledialog

        if value_type == Common.type_int:
            return simpledialog.askinteger(dlg_title, dlg_info,
                                           initialvalue=10)
        elif value_type == Common.type_string:
            return simpledialog.askstring(dlg_title,
                                          dlg_info,
                                          initialvalue='hello world!')
        else:
            raise Exception("unsupport type")

    def messagebox_decorator(func):
        def make_decorater(*args, **kwargs):
            root = tkinter.Tk()
            root.withdraw()
            res_info = func(*args, **kwargs)
            root.destroy()
            return res_info

        return make_decorater

    @classmethod
    @messagebox_decorator
    def messagebox(cls, msg_info, msg_title="info"):
        tkinter.messagebox.showinfo(msg_title, msg_info)

    @classmethod
    @messagebox_decorator
    def messagebox_warning(self, msg_info, msg_title="warning"):
        tkinter.messagebox.showwarning(msg_title, msg_info)

    @classmethod
    @messagebox_decorator
    def messagebox_error(self, msg_info, msg_title="error"):
        tkinter.messagebox.showerror(msg_title, msg_info)

    @classmethod
    @messagebox_decorator
    def messagebox_okcancel(self, msg_info, msg_title="query"):
        return tkinter.messagebox.askokcancel(msg_title, msg_info)

    @classmethod
    @messagebox_decorator
    def messagebox_yesno(self, msg_info, msg_title="query"):
        return tkinter.messagebox.askquestion(msg_title, msg_info)

    @classmethod
    @messagebox_decorator
    def messagebox_yesnocancel(self, msg_info, msg_title="query"):
        return tkinter.messagebox.askyesnocancel(msg_title, msg_info)

    @classmethod
    @messagebox_decorator
    def messagebox_retrycancel(self, msg_info, msg_title="query"):
        return tkinter.messagebox.askretrycancel(msg_title, msg_info)

    @classmethod
    @messagebox_decorator
    def open_file_dialog(cls,
                         filetypes_=[("All Files", "*")],
                         title_="打开文件"):
        return filedialog.askopenfilename(title=title_,
                                          filetypes=filetypes_
                                          )

    @classmethod
    @messagebox_decorator
    def open_files_dialog(cls,
                          filetypes_=[("All Files", "*")],
                          title_="打开多个文件"):
        return filedialog.askopenfilenames(title=title_,
                                           filetypes=filetypes_
                                           )

    @classmethod
    @messagebox_decorator
    def open_directory_dialog(cls):
        return tkinter.filedialog.askdirectory()

    @classmethod
    @messagebox_decorator
    def save_file_dialog(cls):
        return tkinter.filedialog.asksaveasfilename()


class DataViewWidget(object):

    def except_decorator_before_run_win(func):
        def make_decorater(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:

                traceback.print_exc(file=open(Common.err_log_file_name, "w"))

                error_str = ""
                with open(Common.err_log_file_name, "r") as f:
                    while True:
                        buf_str = f.readline()
                        if buf_str:
                            error_str += buf_str
                        else:
                            break
                if not args[0].if_main_win_run:
                    if args[0].root:
                        args[0].root.withdraw()
                    else:
                        tkinter.Tk().withdraw()

                raise

        return make_decorater

    @except_decorator_before_run_win
    def get_screen_size_other_win(self, other_win):
        return other_win.winfo_screenwidth(),
        other_win.winfo_screenheight()

    @except_decorator_before_run_win
    def get_window_size_other_win(self, other_win):
        return other_win.winfo_reqwidth(),
        other_win.winfo_reqheight()

    @except_decorator_before_run_win
    def center_window_other_win(self, other_win, width, height):
        screenwidth = other_win.winfo_screenwidth()
        screenheight = other_win.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height,
                                (screenwidth - width) / 2,
                                (screenheight - height) / 2)
        other_win.geometry(size)

    @except_decorator_before_run_win
    def moveScroll(self, event):
        if event.delta < 0:
            for index, row in enumerate(self.generator_data):
                self.tv.insert('', index + 1, values=tuple(row))
                if (index + 2) > self.show_data_count:
                    break

    @except_decorator_before_run_win
    def treeview_sort_column(self, tv, col, reverse):
        list1 = [(tv.set(k, col), k) for k in tv.get_children('')]
        list1.sort(reverse=reverse)
        for index, (val, k) in enumerate(list1):
            tv.move(k, '', index)
        tv.heading(col,
                   command=lambda: self.treeview_sort_column(tv,
                                                             col, not reverse))

    @except_decorator_before_run_win
    def show_treeview(self, title, columns_name, generator_data,
                      show_data_count=100):
        self.if_main_win_run = False
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("300x300")

        if isinstance(generator_data, list):
            generator_data = (x for x in generator_data)

        self.generator_data = generator_data
        self.show_data_count = show_data_count

        tv_titile = []
        for i in range(len(columns_name)):
            tv_titile.append(str(i))

        self.tv = ttk.Treeview(self.root, height=23,
                               show='headings',
                               columns=tv_titile)

        self.tv.bind("<MouseWheel>", self.moveScroll)

        for i in range(len(columns_name)):
            self.tv.column(tv_titile[i], width=70, anchor='center')
            self.tv.heading(tv_titile[i], text=columns_name[i],
                            command=lambda _col=i: self.treeview_sort_column(self.tv,_col,False))

        for index, row in enumerate(generator_data):
            self.tv.insert('', index + 1, values=tuple(row))
            if (index + 2) > show_data_count:
                break

        vbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.tv.yview)
        self.tv.configure(yscrollcommand=vbar.set)
        self.tv.grid(row=0, column=0, sticky=tk.NSEW)
        vbar.grid(row=0, column=1, sticky=tk.NS)
        hbar = ttk.Scrollbar(self.root, orient=tk.HORIZONTAL,
                             command=self.tv.xview)
        self.tv.configure(xscrollcommand=hbar.set)
        hbar.grid(row=1, column=0, sticky=tk.EW)

        self.root.columnconfigure(0, weight=1)

        self.center_window_other_win(self.root, 600, 500)
        self.root.maxsize(600, 500)
        self.root.minsize(600, 500)

        self.if_main_win_run = True

        self.root.mainloop()


@except_decorator
def test_encry():
    tkinter.messagebox.showinfo('Info', Widget.get_text("text1"))
    Widget.set_text("text1", "text1111111111")


@except_decorator
def hit_me():
    tkinter.messagebox.showinfo(title='Hi', message='你好！')


@except_decorator
def test_select_change(*args):
    tkinter.messagebox.showinfo(title='Hi',
                                message=Widget.get_comboxlist("com41111"))


@except_decorator
def test_checkbox():
    '''
    if Widget.get_checkbox("check5"):
        tkinter.messagebox.showinfo('Info', "True")
    else:
        tkinter.messagebox.showinfo('Info', "False")
    '''
    if Widget.get_checkbox("check1"):
        tkinter.messagebox.showinfo('Info', "True")
    else:
        tkinter.messagebox.showinfo('Info', "False")

    if Widget.get_checkbox("check2"):
        tkinter.messagebox.showinfo('Info', "True")
    else:
        tkinter.messagebox.showinfo('Info', "False")

    if Widget.get_checkbox("check3"):
        tkinter.messagebox.showinfo('Info', "True")
    else:
        tkinter.messagebox.showinfo('Info', "False")

    if Widget.get_checkbox("check4"):
        tkinter.messagebox.showinfo('Info', "True")
    else:
        tkinter.messagebox.showinfo('Info', "False")

    if Widget.get_checkbox("check5"):
        tkinter.messagebox.showinfo('Info', "True")
    else:
        tkinter.messagebox.showinfo('Info', "False")


@except_decorator
def test_main():
    win = Widget()
    win.create_main_win("测试数据处理", 500)
    win.add_text("text1")
    win.add_button("处理", test_encry)
    win.add_label_text("测试说明测试说明", "test5")
    comboxlist_item = ["中国人", "古巴人", "美国人", "日本人", "韩国人"]
    win.add_comboxlist("com1", comboxlist_item, test_select_change)
    win.add_label_comboxlist("COMBOX测试说明", "com3", comboxlist_item)
    c_box = [["check1", "check1"], ["C++", "check2"], ["java", "check3"]]
    c_box.append(["vba", "check4"])
    win.add_checkbox(c_box)
    win.add_text_button("text3", "按钮2", hit_me)
    win.add_button("测试checkboc", test_checkbox)

    win.run_main_win()


if __name__ == '__main__':
    test_main()
