#!/usr/bin/env python3
import pathlib, os


def create_dir(directory):
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)


def get_files_list(directory='/', extensions='', startswith='',
                   abs_path=False, sub_dirs=False, exclude_dirs=[]):
    """
    Retrieves a list of files for a given directory.

    Args:
        (str) directory - Path of directory to find files. Defaults to root directory.
        (Tuple) extensions - Extensions to include (eg. txt). Includes all extensions by default.
        (str) startswith - File name must begin with this string.
        (bool) abs_path - Set to true if provided directory is an absolute path. Defaults to false for relative path.
        (bool) sub_dirs - Set to true to include files in sub directories. Defaults to false.
        (list) exclude_dirs - List of directories to exclude. This only applies if sub_dirs is True.
    Returns:
        files - List of files in specified directory.
    """

    file_dir = ''
    if abs_path:
        file_dir = directory
    if sub_dirs:
        files = [os.path.join(root, f)
                 for root, dirs, files in os.walk(directory)
                 for f in files
                 if f.startswith(startswith) and f.endswith(extensions)]

        files[:] = [f for f in files if os.path.basename(os.path.dirname(f)) not in exclude_dirs]
    else:
        files = [file_dir + f for f in os.listdir(directory)
                 if f.startswith(startswith) and f.endswith(extensions)]
    return files


def get_subdirectories(directory):
    return [name for name in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, name))]


def read_conf_file(path, keywords=[], delimitor='='):
    conf = {}

    def read_line(line):
        for keyword in keywords:
            kd = keyword.lower() + delimitor
            if kd in line.lower():
                value = line.lower().split(kd)[-1].rstrip('\n')
                conf[keyword] = value

    with open(path) as f:
        for line in f:
            read_line(line)

    return conf


def create_text_file(path, text):
    file = open(path, 'w')
    file.writelines(text)
    file.close()