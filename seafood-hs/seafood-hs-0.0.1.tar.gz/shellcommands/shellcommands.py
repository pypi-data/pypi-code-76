# -*- coding: utf-8 -*-
r"""
library for shell commands and sub processes.
Adapted from Moritz Goerzen's library 08.2018 (Spintronic Theory Kiel).
"""
import os
import platform
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Union, TypeVar

PathLike = TypeVar("PathLike", str, Path)

# operating system
OPERATINGSYSTEM = platform.system()


@contextmanager
def change_directory(newdir: PathLike) -> None:
    r"""
    Changes the directory using context manager. Will automatically put everything before the yield statement into the
    __enter__-method and everythin behind in the __exit__method.

    Args:
        newdir(str): name of the directory. Has to be a subdirectory of the actual directory.
    """
    prevdir = Path.cwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


def copy_element(target: PathLike, destination: PathLike) -> None:
    r"""
    Copies an element (target) to a destination. Chooses the command based on OS. On windows the shell=True flag
    must be set. Should be replaced someday by shutil.which
    (https://stackoverflow.com/questions/3022013/windows-cant-find-the-file-on-subprocess-call)

    Args:
        target(PathLike): target file
        destination(PathLike): destination file
    """
    if OPERATINGSYSTEM == 'Windows':
        command = "copy " + str(target) + " " + str(destination)
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, shell=True)
    elif OPERATINGSYSTEM == 'Linux':
        command = "cp " + str(target) + " " + str(destination)
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    else:
        raise Exception('operating system not yet coded.')
    output, error = process.communicate()
