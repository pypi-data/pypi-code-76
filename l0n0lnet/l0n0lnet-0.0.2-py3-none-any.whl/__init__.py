from ctypes import *

import os
import platform
import sys

cur_file_path, filename = os.path.split(os.path.abspath(__file__))

if platform.system() == "Windows":
    if platform.architecture()[0] == "64bit":
        se = cdll.LoadLibrary(f"{cur_file_path}/libse_windows_x64.so")
    else:
        se = cdll.LoadLibrary(f"{cur_file_path}/libse_windows_x86.so")
elif platform.system() == "Linux":
    if platform.machine() == "x86_64" or platform.machine() == "AMD64":
        se = cdll.LoadLibrary(f"{cur_file_path}/libse_linux_x64.so")
    elif platform.machine() == "aarch64":
        se = cdll.LoadLibrary(f"{cur_file_path}/libse_linux_armv7.so")
    else:
        sys.stderr.write(("Current platform not supported.\n"))
else:
    sys.stderr.write(("Current platform not supported.\n"))

se.create_server_v4.restype = c_uint32
se.create_server_v4.argtypes = [c_char_p, c_int32, c_int32]

se.connect_to_v4.restype = c_uint32
se.connect_to_v4.argtypes = [c_char_p, c_int32]

se.close_tcp.restype = None
se.close_tcp.argtypes = [c_int32]

se.send_message.restype = c_bool
se.send_message.argtypes = [c_uint32, c_char_p, c_size_t]

se.call_after.restype = c_bool

se.quit.restype = None


def run():
    """
    用来启动程序，会卡线程
    """
    se.run()


def run_nowait():
    """
    用来启动程序，不卡线程
    """
    se.run_nowait()


_delay_funcs = {}
_max_delay_id = 0


@CFUNCTYPE(None, c_uint64)
def _delay_cb(id):
    data = _delay_funcs.get(id)
    if not data:
        return

    data['cb']()

    if data['repeat'] == 0:
        del _delay_funcs[id]


def call_after(timeout: int, fn, repeat: int = 0):
    """
    延时调用

    @timeout:int: timeout毫秒后调用fn函数\n
    @fn: function: 无参数，无返回值的函数\n
    @repeat: int: repeat毫秒后重复执行该函数\n

    例如：
    ```
    def test_timer():
        print("123")

    # 每秒打印一次 '123'
    call_after(1000, test_timer, 1000)

    ```
    """
    global _max_delay_id
    _max_delay_id = _max_delay_id + 1

    _delay_funcs[_max_delay_id] = {
        "cb": fn,
        "repeat": repeat
    }

    se.call_after(timeout, _delay_cb, _max_delay_id, repeat)


close_funcs = []


@CFUNCTYPE(None)
def on_quit():
    for func in close_funcs:
        func()


se.set_on_quit(on_quit)


def add_quit_func(func):
    close_funcs.append(func)
