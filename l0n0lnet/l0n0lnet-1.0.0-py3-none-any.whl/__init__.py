from ctypes import *

import os
import platform
import sys
import base64

cur_file_path, filename = os.path.split(os.path.abspath(__file__))

lib_temp_path = None

if platform.system() == "Windows":
    if platform.architecture()[0] == "64bit":
        from l0n0lnet.libse_windows_x64 import libse_data
    else:
        from l0n0lnet.libse_windows_x86 import libse_data
    lib_temp_path = os.environ.get("TEMP") + "\\l0n0lnet"
elif platform.system() == "Linux":
    if platform.machine() == "x86_64" or platform.machine() == "AMD64":
        from l0n0lnet.libse_linux_x64 import libse_data
    elif platform.machine() == "aarch64":
        from l0n0lnet.libse_linux_armv7 import libse_data
    else:
        sys.stderr.write(("Current platform not supported.\n"))
    lib_temp_path = "/tmp/l0n0lnet"

else:
    sys.stderr.write(("Current platform not supported.\n"))

# 创建缓存目录
if not os.path.exists(lib_temp_path):
    os.mkdir(lib_temp_path)

# 写入库内容
libpath = f"{lib_temp_path}/libse_1.so"
with open(libpath, 'wb') as fp:
    fp.write(base64.decodebytes(libse_data))

# 加载库
se = cdll.LoadLibrary(libpath)

# 初始化库
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
