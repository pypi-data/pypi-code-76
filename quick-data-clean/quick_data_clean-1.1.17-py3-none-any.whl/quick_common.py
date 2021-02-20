# -*- coding: utf-8 -*-

import sys
import tkinter.messagebox
import traceback
import time


test_data_path = r"C:\data_test"
test_data_path += "\\"

class EasyBacic(object):
    def __init__(self):
        sys.stderr = RedirectStdOutStdError()
        sys.stdout = RedirectStdOutStdError()


class WidgetException(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo


class Common(object):

    type_int = 0
    type_string = 1
    type_list = 2
    type_function = 3
    type_byte = 4

    log_file_name = "quick_data_clean.log"
    err_log_file_name = "quick_data_clean.err"

    @classmethod
    def TraceStack(cls):
        frame = sys._getframe(1)
        trace_str = "\n" + "TraceStackInfo:" + "\n"
        current_level = False
        while frame:

            if current_level:
                current_level = False
            else:
                fiename_str = frame.f_code.co_filename + " "
                funcname_str = frame.f_code.co_name + " "
                fileline_str = str(frame.f_lineno) + " "
                trace_str += "File \"{0}\",line {1} ,in {2}\n".format(
                    fiename_str,
                    fileline_str,
                    funcname_str)
            frame = frame.f_back
        return trace_str

    @classmethod
    def check_assign_type(cls, var_name, type_index, info):

        if type_index == cls.type_int:
            if not isinstance(var_name, int):
                raise Exception("{0} must be a int.".format(info))
        elif type_index == cls.type_string:
            if not isinstance(var_name, str):
                raise Exception("{0} must be a "
                                "string.".format(info))
        elif type_index == cls.type_list:
            if not isinstance(var_name, list):
                raise Exception("{0} must be a "
                                "list.".format(info))
        elif type_index == cls.type_function:
            if (str(type(var_name)) != "<class 'function'>"):
                raise Exception("{0} must be a "
                                "function.".format(info))
        elif type_index == cls.type_byte:
            if not isinstance(var_name, bytes):
                raise Exception("{0} must be a "
                                "bytes.".format(info))

    @classmethod
    def get_python_except_info(cls, e_obj):
        exc_type, exc_value, exc_traceback = sys.exc_info()

        error_str = ""

        error_str += "error_type: " + exc_type.__name__ + "\n"
        error_str += "error_msg: " + str(e_obj) + "\n"

        return error_str

    @classmethod
    def get_error_info(cls, e_obj):
        error_from_e_str = str(e_obj)
        error_str = ""
        if error_from_e_str.find("TraceStackInfo:") < 0:
            error_str = "Exception from the python: \n"
            error_str += Common.get_python_except_info(e_obj)
            error_str += cls.TraceStack()

        else:
            error_str = error_from_e_str

        return error_str


def except_decorator_main_win(func):
    def make_decorater(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except WidgetException:
            pass
        except Exception:

            traceback.print_exc(file=open(Common.err_log_file_name, "w",
                                          encoding="utf-8"))

            error_str = ""
            with open(Common.err_log_file_name, "r", encoding="utf-8") as f:
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

            tkinter.messagebox.showerror(title='Error',
                                         message=error_str)

    return make_decorater


def except_decorator(func):
    def make_decorater(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except WidgetException:
            pass
        except Exception:
            traceback.print_exc(file=open(Common.err_log_file_name, "w",
                                          encoding="utf-8"))

            error_str = ""
            with open(Common.err_log_file_name, "r", encoding="utf-8") as f:
                while True:
                    buf_str = f.readline()
                    if buf_str:
                        error_str += buf_str
                    else:
                        break
            root = tkinter.Tk()
            root.withdraw()
            tkinter.messagebox.showerror(title='Error',
                                         message=error_str)
            root.destroy()

    return make_decorater


#def except_decorator_clear(*dargs, **dkargs):
def except_decorator_clear(clear_func):
    def make_decorater(func):
        def _make_decorater(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except WidgetException:
                pass
            except Exception:

                if(hasattr(clear_func, '__call__')):
                    clear_func()

                traceback.print_exc(file=open(Common.err_log_file_name, "w",
                                              encoding="utf-8"))

                error_str = ""
                with open(Common.err_log_file_name, "r", encoding="utf-8") as f:
                    while True:
                        buf_str = f.readline()
                        if buf_str:
                            error_str += buf_str
                        else:
                            break
                root = tkinter.Tk()
                root.withdraw()
                tkinter.messagebox.showerror(title='Error',
                                             message=error_str)
                root.destroy()
        return _make_decorater

    return make_decorater


def func_time_decorator(func):
    def make_decorater(*args, **kwargs):
        start = time.clock()
        func(*args, **kwargs)
        elapsed = (time.clock() - start)
        print("Time used: {:.2f} seconds".format(elapsed))
    return make_decorater


class RedirectStdOutStdError(object):
    def __init__(self, filename=Common.log_file_name):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass
