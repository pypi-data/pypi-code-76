# This file contains a collection of helper functions that are not tested

import os
from os import listdir
from os.path import isfile, join
from typing import List


def root_dir() -> str:
    """
    Gets the root dir of the project
    :return: str
    """
    return os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + "/../..")


def file_contents(file: str) -> str:
    """
    Gets contents from a file
    :param file: str
    :return: str
    """
    return open(file, "r").read()


def dir_files(folder: str) -> List[str]:
    """
    Gets a directories files
    :param folder: str
    :return: list[str]
    """
    files = []
    file: str
    for file in listdir(folder):
        path_full = join(folder, file)
        if isfile(path_full):
            files.append(file)
    return files


def dir_exists(folder: str) -> bool:
    """
    Does a dir exist
    :param folder:
    :return:
    """
    return os.path.exists(folder)


def write_to_standard_out(message: str):
    """
    Writes a message to standard out
    :param message: str
    :return: void
    """
    print(message)
