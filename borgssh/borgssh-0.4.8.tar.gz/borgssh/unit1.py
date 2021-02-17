#!/usr/bin/env python3
from borgssh.version import __version__
from fire import Fire

from borgssh.prj_utils import get_file_path
from borgssh.prj_utils import fail
from borgssh.prj_utils import Bcolors
from borgssh.prj_utils import super_print

print("i... unit uname loaded, version:",__version__)

def func(debug = False):

    global print
    print=super_print(debug)(print)

    print("D... in function func DEBUG may be filtered")
    print("i... in function func")
    return True

def test_func():
    print("i... TESTING function func")
    assert func() == True

if __name__ == "__main__":
    print("i... in the __main__ of uname of borgssh")
    Fire()

    