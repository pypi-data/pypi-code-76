# Save and resume progress in lightcards
# Armaan Bhojwani 2021

import hashlib
import os
import pickle

xdg = os.environ.get("XDG_CACHE_HOME")
if xdg:
    dired = f"{os.path.expanduser('~')}/{xdg}/lightcards/"
else:
    dired = f"{os.path.expanduser('~')}/.cache/lightcards/"


def name_gen(stra):
    """Generate hash of stack for name of pickle file"""
    return hashlib.md5(str([str(x) for x in stra]).encode("utf-8")).hexdigest()


def make_dirs(dired):
    """mkdir -p equivalent"""
    if not os.path.exists(dired):
        os.makedirs(dired)


def dump(obj, stra):
    """Write pickle file"""
    make_dirs(dired)

    pickle.dump(obj, open(f"{dired}/{name_gen(stra)}.p", "wb"))


def dive(stra):
    """Get pickle file"""
    file = f"{dired}/{name_gen(stra)}.p"
    make_dirs(dired)
    if os.path.exists(file):
        return pickle.load(open(file, "rb"))
    else:
        return False


def purge(stra):
    """Delete pickle file"""
    file = f"{dired}/{name_gen(stra)}.p"
    if os.path.exists(file):
        os.remove(file)
