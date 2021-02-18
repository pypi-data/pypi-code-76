from .discover_net import DiscoverNet as Discover
from .repl import ReplException
from .config_store import Config

from serial import SerialException
import sys
import time
import threading

import logging

logger = logging.getLogger(__file__)


class Output:
    def ans(self, value):
        if isinstance(value, bytes): value = value.decode()
        print(value, flush=True, end="")

    def err(self, value):
        if isinstance(value, bytes): value = value.decode()
        print(value, flush=True, end="")

code = [

b"print(2**10)",

"""
for i in range(3):
    print(i, i**2, i**3)
""",

"print('4/sf)",

"""import time
time.sleep(2)""",

"a = 5",
"print(a)",
"softreset",
"print(a)"

]

def demo_eval(repl):
    for c in code:
        print('-'*50)
        try:
            if c == "softreset":
                print("SOFTRESET")
                repl.softreset()
            elif c == "uid":
                print(f"UID {repl.uid}")
            else:
                print(f"EVAL {c}")
                repl.eval(c, Output())
        except ReplException as re:
            print(f"***** ERROR {re}")

def listfiles():
    # this function runs on the MCU ...
    from os import listdir
    return listdir()

def demo_functions(repl):
    print(f"listfiles (on mcu): {repl.eval_func(listfiles)}")
    fn = 'boot.py'
    print(f"cat({fn}):")
    repl.cat(Output(), fn)
    if (True): return
    print('\n', '-'*10)
    fn = 'delete_me.txt'
    repl.fget('lib/adafruit_requests.py', f'tmp/{fn}')
    print('\n', '-'*10)
    fn = 'delete_me.txt'
    repl.fput(f'tmp/{fn}', fn)
    print('\n', '-'*10)
    print(f"cat({fn})")
    repl.cat(Output(), fn)
    print(f"new file {fn} on mcu ...")
    print(f"listfiles: {repl.eval_func(listfiles)}")
    print("after rm ...")
    repl.rm_rf(fn)
    print(f"listfiles: {repl.eval_func(listfiles)}")

def demo_rsync(repl):
    # sync time ...
    print(f"before sync: get_time = {repl.get_time()}")
    repl.sync_time()
    print(f"after  sync: get_time = {repl.get_time()}")
    # rsync
    print('-'*10, 'rlist')
    repl.rlist(Output())
    print('-'*10, 'rdiff')
    repl.rdiff(Output())
    print('-'*10, 'rsync')
    repl.rsync(Output())

def main():

    # configure logging

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


    # configure device scanner

    discover = Discover()

    def scanner():
        while True:
            discover.scan()
            time.sleep(Config.get('device_scan_interval', 1.0))

    threading.Thread(target=scanner, daemon=True).start()

    # run code on all discovered devices
    while (True):
        with discover as devices:
            if len(devices) < 1:
                print("no devices on-line ...")
                time.sleep(1)
            for dev in devices:
                print(f"\n{'-'*50} {dev}, age = {dev.age}:")
                if dev.locked:
                    print("device busy, skipping")
                    continue
                with dev as repl:
                    try:
                        demo_eval(repl)
                        demo_functions(repl)
                        demo_rsync(repl)
                    except SerialException as se:
                        print(f"SerialException in DiscoverSerial.main: {se}")
                    except ConnectionResetError as cre:
                        print(f"ConnectionResetError in DiscoverSerial.main: {cre}")
                    except OSError as oe:
                        print(f"OSError in DiscoverSerial.main: {oe}")
        time.sleep(5)

if __name__ == "__main__":
    main()