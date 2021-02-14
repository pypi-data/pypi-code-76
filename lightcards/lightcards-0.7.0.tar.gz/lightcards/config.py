# Parse lightcards config file
# Armaan Bhojwani 2021

import sys
from pathlib import Path
import os


class ConfigException(BaseException):
    def __init__(self, message):
        self.message = message
        print(f"lightcards: {self.message}")
        sys.exit(4)


def read_file(file):
    config = {}
    file = str(file)
    files = []
    local_xdg = f"{os.path.expanduser('~')}/{os.environ.get('XDG_CACHE_HOME')}/lightcards/config.py"
    local = f"{os.path.expanduser('~')}/.config/lightcards/config.py"
    world = "/etc/lightcards/config.py"

    if os.path.exists(world):
        files.append(world)
    if os.path.exists(local_xdg):
        files.append(local_xdg)
    if os.path.exists(local):
        files.append(local)

    files.append(file)
    if not os.path.exists(file):
        raise ConfigException(f'"{file}": No such file or directory') from None

    for f in files:
        exec(Path(str(f)).read_text(), {}, config)

    return config
