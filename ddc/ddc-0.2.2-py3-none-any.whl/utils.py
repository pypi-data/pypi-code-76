import pathlib
import pathspec
import logging
import platform
import subprocess
import sys
from os.path import expanduser
import os
import time
import hashlib


def __get_os():
    if os.name == "nt":
        return "windows"

    if platform.system() == "Darwin":
        return "macos"

    return "linux"


OS_NAME = __get_os()
DDC_DIR = "/.ddc/"


def __build_path(path):
    if OS_NAME == "windows":
        path = path.replace("/", "\\")
    full_path = expanduser("~") + path
    return full_path


def read_ddc_file(path) -> str:
    """
    :param path:  example: "developer_settings.json"
    :return: dict
    """
    ret = None
    full_path = __build_path(DDC_DIR + path)
    if os.path.isfile(full_path):
        with open(full_path, "r") as myfile:
            ret = myfile.read()
    return ret


def write_ddc_file(path, value: str) -> None:
    """
    :param path:  example: "developer_settings.json"
    :param value: dict
    """
    ddc_dir = __build_path(DDC_DIR)
    os.makedirs(ddc_dir, exist_ok=True)
    full_path = __build_path(DDC_DIR + path)
    with open(full_path, "w") as myfile:
        myfile.write(value)


def get_path_ddc_file(path) -> str:
    """
    :param path:  example: "developer_settings.json"
    """
    return __build_path(DDC_DIR + path)


def exec_cmd(cmd, print_exec_cmd=True):
    if print_exec_cmd:
        logging.info("Run cmd: " + cmd)
    return subprocess.getstatusoutput(cmd)


def stream_exec_cmd(cmd: str, print_exec_cmd=True):
    if print_exec_cmd:
        logging.info("Run cmd: " + str(cmd))

    # если надо будет печатать на экран в момент выполенения, то подменить subprocess.PIPE на что-то свое
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        universal_newlines=True,
    )
    (out, err) = proc.communicate()
    return proc.returncode, out + "\n" + err


def run_if_time_has_passed(lock_key: str, ttl_min: int, callback_fn):
    """Run callback function is lock time is passed"""
    lock_file = "fce_" + lock_key + ".loc"
    current_ts = int(time.time())
    saved_ts = read_ddc_file(lock_file)
    if not saved_ts:
        saved_ts = 0
    else:
        saved_ts = int(saved_ts)
    if current_ts - saved_ts > ttl_min * 60:
        callback_fn()
        write_ddc_file(lock_file, str(current_ts))


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


def iterate_source_files_with_gitignore(base_path: str):
    """
    Iterate all files in base_path including hidden dir and files.
    Using .gitignore for skip items.
    """
    gitignores = []
    # glob.glob skip hidden files. We can't use it.
    for fileref in pathlib.Path(base_path).glob("**/*.*"):
        file = str(fileref)
        if file.endswith(".gitignore"):
            with open(file, "r") as f:
                spec_lines = []
                for line in f.readlines():
                    line = line.strip()
                    if line.endswith("*"):
                        line = line.rstrip("*")
                    spec_lines.append(line)

            spec = pathspec.PathSpec.from_lines("gitwildmatch", spec_lines)
            git_ignore_dir = file[0 : -len(".gitignore")]
            gitignores.append(
                {"dir": git_ignore_dir, "dir_len": len(git_ignore_dir), "spec": spec}
            )
            continue

        is_ignored_file = False
        for git_ignore_info in gitignores:
            if file.startswith(git_ignore_info["dir"]):
                cutted_file = file[git_ignore_info["dir_len"] :]
                is_ignored_file = git_ignore_info["spec"].match_file(cutted_file)
                if is_ignored_file:
                    break
        if is_ignored_file:
            continue
        yield file


def get_exists_langs(base_path: str):
    """
    Compute which languages use in base_path
    """
    extensions = {
        "js": False,
        "ts": False,
        "java": False,
        "php": False,
        "py": False,
        "go": False,
    }
    for file in iterate_source_files_with_gitignore(base_path):
        for f_ext, is_found in extensions.items():
            if not is_found:
                if file.endswith("." + f_ext):
                    extensions[f_ext] = True

    langs = []
    for ext_name, ext_exists in extensions.items():
        if ext_exists:
            langs.append(ext_name)
    return langs


def get_lang_tests_dir(base_path: str):
    """
    Get list of folders with langs for run tests
    """
    dirs = {}

    def discover_py_php(file: str):
        # folder with tests MUST be named as "/tests"
        if "/tests" not in file:
            return

        parts = file.split("/")
        parts_cnt = len(parts)
        if parts_cnt < 2:
            return

        dirname = parts[parts_cnt - 2]
        if dirname != "tests":
            return

        filename = parts[parts_cnt - 1]
        dir_ = "/".join(parts[0:-2])

        if filename == "bootstrap.php":
            dirs[dir_] = {"lang": "php", "dir_for_run_tests": dir_}

        if filename == "__init__.py":
            dirs[dir_] = {"lang": "py", "dir_for_run_tests": dir_}

        if filename.startswith("test_") and filename.endswith(".py"):
            dirs[dir_] = {"lang": "py", "dir_for_run_tests": dir_}

    def discover_java(file: str):
        # folder with tests MUST be named as "/src/test/java"
        if "/src/test/java" not in file:
            return
        if not file.endswith(".java"):
            return
        # find root java module
        parts = file.split("/src/test/java")
        if len(parts) > 0:
            dir_ = parts[0]
            dirs[dir_] = {"lang": "java", "dir_for_run_tests": dir_}

    for file in iterate_source_files_with_gitignore(base_path):
        discover_py_php(file)
        discover_java(file)

    return list(dirs.values())


def md5(input_str: str):
    return hashlib.md5(input_str.encode("utf-8")).hexdigest()
