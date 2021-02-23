"""
Utils for creating a list of data_files
"""

__all__ = [
    "get_data_files",
    "add_to_data_files",
]

import os

DATA_FILES = {}


def is_subdir(path, cwd=None):
    """returns true if the path is a subdirectory of cwd"""
    cwd = cwd or os.getcwd()
    path = os.path.realpath(path)
    return cwd == path or path.startswith(cwd + os.sep)


def _add_to_data_files(directory, filename):
    "Auxiliary function for adding to DATA_FILES"
    assert is_subdir(directory), "Given directory is not a subdir %s" % directory
    if directory in DATA_FILES:
        if filename not in DATA_FILES[directory]:
            DATA_FILES[directory].append(filename)
    else:
        DATA_FILES[directory] = [filename]


def add_to_data_files(*files, directory=None):
    """Stores the given files into the DATA_FILES variable.
    Use get_data_files() to access the list of data_files."""
    for filename in files:
        if isinstance(filename, tuple):
            assert len(filename) == 2
            add_to_data_files(*filename[1], directory=filename[0])
        elif directory:
            _add_to_data_files(directory, filename)
        else:
            assert is_subdir(
                filename
            ), "If directory is not given, then the file must be in a subdir"
            filename = os.path.realpath(filename)[len(os.getcwd()) + 1 :].split(os.sep)
            if len(filename) == 1:
                _add_to_data_files(".", filename[0])
            else:
                _add_to_data_files(os.sep.join(filename[:-1]), os.sep.join(filename))


def get_data_files():
    "Returns the list of data_files"
    return list(DATA_FILES.items())
