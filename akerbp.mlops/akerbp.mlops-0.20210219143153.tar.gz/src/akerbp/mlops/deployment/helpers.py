# helpers.py
import sys
import os
from pathlib import Path

from importlib import import_module, resources as importlib_resources
import shutil
import subprocess

from akerbp.mlops.core import logger, config 


logging=logger.get_logger(name='mlops_deployment')

env = config.envs.env
service_name = config.envs.service_name


def get_version():
    tag = subprocess.check_output(
        ['git', 'describe', '--tags', '--abbrev=0'],
        encoding='UTF-8'
    ).rstrip()
    if env in ['dev', 'test']:
        version = '0.' + tag
    elif env == 'prod':
        version = '1.' + tag
    return version


def get_repo_origin():
    origin = subprocess.check_output(
        ['git', 'remote', 'get-url', '--push', 'origin'],
        encoding='UTF-8'
    ).rstrip()
    return origin


def replace_string_file(s_old, s_new, file):
    """
    Replaces all occurrences of s_old with s_new in a file
    """
    with open(file) as f:
        s = f.read()
        if s_old not in s:
            logging.warning(f"Didn't find '{s_old}' in {file}")

    with open(file, 'w') as f:
        s = s.replace(s_old, s_new)
        f.write(s)


def set_mlops_import(req_file):
    package_version = get_version()
    replace_string_file('MLOPS_VERSION', package_version, req_file)
    logging.info(f"Set akerbp.mlops=={package_version} in requirements.txt")


def to_folder(path, folder_path):
    """
    Copy folders, files or package data to a given folder.
    Note that if target exists it will be overwritten.
    Input:
      - path: supported formats
            - folder path (string): e,g, "my/folder" 
            - file path (string): e.g. "my/file" (string)
            - module file (tuple/list): e.g. ("my.module", "my_file") 
    """
    if isinstance(path,(tuple,list)):
        if importlib_resources.is_resource(*path):
            with importlib_resources.path(*path) as file_path:
                shutil.copy(file_path, folder_path)
        else:
            raise ValueError(f"Didn't find {path[1]} in {path[0]}")
    elif os.path.isdir(path):
        shutil.copytree(
            path, 
            os.path.join(folder_path, path), 
            dirs_exist_ok=True
        )
    elif os.path.isfile(path):
        shutil.copy(path, folder_path)
    else:
        raise ValueError(f"{path} should be a file, folder or package resource")


def copy_to_deployment_folder(files, deployment_folder):
    """
    Copy a list of files to a deployment folder
    List of files is given as a dictionary where the key is the nick name of the file (will be used for logging) and the value is the path.
    """
    for k,v in files.items():
        logging.debug(f"{k} => deployment folder")
        to_folder(v, deployment_folder)


def run_tests(test_path, path_type='file'):
    """
    Run tests with pytest
    Input
      - test_path: path to tests with pytest (string or a list of strings) All
        should have the same format (see next parameter)
      - path_type: either 'file' (test_path refers then to files/folders) or
        'module' (test_path refers then to modules)
    """
    command = [sys.executable, "-m", "pytest", 
                "--quiet", "--color=no", "-W ignore:numpy.ufunc size changed"]
    if path_type == 'module':
        command.append("--pyargs")
    if isinstance(test_path, str) or isinstance(test_path, Path):
        command.append(test_path)
    elif isinstance(test_path, list):
        command += test_path
    else:
        raise ValueError("Input should be string or list of strings")
    logging.info(f"Run tests: {test_path}")
    subprocess.check_call(command)


def install_requirements(req_file):
    logging.info(f"Install python requirement file {req_file}")
    c = ["pip", "install", "--quiet", "-r", req_file]
    subprocess.check_call(c)


def set_up_requirements(c):
    """
    Set up a "requirements.txt" file at the top of the deployment folder
    (assumed to be the current directory) and install dependencies (unless in
    dev)
    """
    logging.info("Create requirement file")
    set_mlops_import(c.req_file)
    shutil.move(c.req_file, 'requirements.txt')
    c.req_file = 'requirements.txt'
    if env != "dev":
        install_requirements('requirements.txt')



def get_model_test_data(test_import_path):
    service_test = import_module(test_import_path).ServiceTest()
    input = getattr(service_test, f"{service_name}_input")
    check = getattr(service_test, f"{service_name}_check")
    return input, check