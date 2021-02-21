#!/usr/bin/env python3

import os, sys

DATA_PIPE = "/var/run/mumble_ptt_caps_lock_led.pipe"

LED_SYS_DIR = "/sys/class/leds/"
LED_SYS_MAX_BRIGHTNESS = "/max_brightness"
LED_SYS_BRIGHTNESS = "/brightness"

def set_caps_led(state: bool, folder: str):
    brightness = "0"
    if state:
        with open(folder + LED_SYS_MAX_BRIGHTNESS) as f:
            brightness = f.read()

    with open(folder + LED_SYS_BRIGHTNESS, 'w') as f:
        f.write(brightness)

def set_all_caps_leds(state: bool):
    for filename in os.listdir(LED_SYS_DIR):
        if filename.endswith("::capslock"):
            set_caps_led(state, LED_SYS_DIR + filename)

def run():
    while True:
        with open(DATA_PIPE, 'r') as f:
            while True:
                c = f.read(1)
                if len(c) < 1:
                    break
                if c == "1":
                    set_all_caps_leds(True)
                elif c == "0":
                    set_all_caps_leds(False)
                else:
                    print("Got character '{}'. Ignoring".format(c))

def main():
    if os.path.exists(DATA_PIPE):
        print("Pipe exists. Removing.")
        os.remove(DATA_PIPE)
    os.mkfifo(DATA_PIPE)
    os.chmod(DATA_PIPE, 0o666)
    try:
        run()
    finally:
        os.remove(DATA_PIPE)

if __name__ == "__main__":
    main()
