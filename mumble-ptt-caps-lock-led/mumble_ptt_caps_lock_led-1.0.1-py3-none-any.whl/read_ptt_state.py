#!/usr/bin/env python3

from time import sleep

import stat, os

from pydbus import SessionBus
from gi.repository import GLib

STATUS_NOTIFIER_SERVICE_SUBSTRING = "StatusNotifierItem"
STATUS_NOTIFIER_PATH = "/StatusNotifierItem"
STATUS_NOTIFIER_MUMBLE_ID = "Mumble"

SPEAKING_ICON_PIXELS = [0, 0, 0, 0, 82, 68, 162, 243, 3, 85, 170, 255, 4, 64, 191, 255]

CHECK_MUMBLE_ALIVE_PERIOD = 1
CHECK_NEW_MUMBLE_EXISTS_PERIOD = 5

DATA_PIPE = "/var/run/mumble_ptt_caps_lock_led.pipe"

bus = SessionBus()

data_pipe_fd = None

def handle_new_icon(status_notifier_item):
    try:
        pixeldata_list = status_notifier_item.IconPixmap[0][2]
    except:
        return False

    start_of_pixeldata = pixeldata_list[:len(SPEAKING_ICON_PIXELS)]
    message = "0"
    if start_of_pixeldata == SPEAKING_ICON_PIXELS:
        message = "1"

    if not stat.S_ISFIFO(os.stat(DATA_PIPE).st_mode):
        raise ValueError("The file {} is not a fifo named pipe".format(DATA_PIPE))

    data_pipe_fd.write(message)
    data_pipe_fd.flush()


def stop_loop_if_notifier_is_dead(loop, notifier):
    try:
        notifier.Ping()
        return True
    except:
        loop.quit()

def watch_mumble_status_notifier(status_notifier_item):
    status_notifier_item.NewIcon.connect(lambda : handle_new_icon(status_notifier_item))
    loop = GLib.MainLoop()
    GLib.timeout_add(CHECK_MUMBLE_ALIVE_PERIOD, lambda: stop_loop_if_notifier_is_dead(loop, status_notifier_item))
    loop.run()

def find_mumble_status_notifier():
    names = bus.dbus.ListNames()
    for name in names:
        if STATUS_NOTIFIER_SERVICE_SUBSTRING in name:
            status_notifier_item = bus.get(name, STATUS_NOTIFIER_PATH)
            if status_notifier_item.Id == STATUS_NOTIFIER_MUMBLE_ID:
                return status_notifier_item
    return None

def main():
    with open(DATA_PIPE, 'w') as f:
        global data_pipe_fd
        data_pipe_fd = f
        while True:
            status_notifier_item = find_mumble_status_notifier()
            if status_notifier_item is not None:
                # Blocks until mumble_status_notifier is dead
                watch_mumble_status_notifier(status_notifier_item)
            sleep(CHECK_NEW_MUMBLE_EXISTS_PERIOD)

if __name__ == "__main__":
    main()
