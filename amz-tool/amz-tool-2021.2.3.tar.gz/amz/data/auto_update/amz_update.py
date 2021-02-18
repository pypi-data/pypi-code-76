#!/usr/bin/env python3

import json
import os
import sys
import re
import subprocess as sp
from time import sleep
from urllib.request import urlopen
from distutils.dir_util import copy_tree

from packaging.version import parse as ver_parse

# Import blank for fetching pkg dir
import amz

# Declare Some Dirs
AMZ_DATA_DIR = os.environ['HOME'] + '/.amz/data'
AMZ_CONFIG_DIR = os.environ['HOME'] + '/.amz/config'
AMZ_PKG_DIR = os.path.dirname(amz.__file__)


# Define helper functions
def substitute_in_file(replace_str, replace_with, filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            filedata = file.read()
        filedata = filedata.replace(replace_str, replace_with)
        with open(filepath, 'w') as file:
            file.write(filedata)


def get_version():
    with open(f'{AMZ_PKG_DIR}/data/VERSION') as ver:
        v = ver.readlines()[0]
    return v


# Wait for internet
for t in range(10):
    try:
        _ = urlopen('https://pypi.org/pypi/amz-tool/json', timeout=5)
    except:
        print(f'Error with internet connection - trying {t}')
        sleep(600)
        if t == 9:
            print('Error with internet connection - better luck tomorrow')
            sys.exit(1)

# Check if amz package is updateable
# Get current version
amz_current = get_version()

# Get latest version available
amz_latest_data = json.load(urlopen('https://pypi.org/pypi/amz-tool/json'))
amz_latest = amz_latest_data['info']['version']

if ver_parse(amz_current) < ver_parse(amz_latest):
    # Upgrade via pip
    p = sp.run('python3 -m pip install -U amz-tool', shell=True)
    if p.returncode != 0:
        print('Error upgrading amz-tool via pip')
        sys.exit(p.returncode)

    # Copy Data
    try:
        # Copy data into .amz dir
        copy_tree(f'{AMZ_PKG_DIR}/data', AMZ_DATA_DIR)
        # Update vars in pre-commit yaml config
        substitute_in_file('AMZ_DATA_DIR', AMZ_DATA_DIR, f'{AMZ_DATA_DIR}/githooks/config/.pre-commit-config.yaml')
    except:
        print('Error copying amz data')
        sys.exit(1)

    # For repo in amz repos, copy config files
    try:
        # Fetch all AMZ Repos - without using yaml
        # TODO: BAD way of parsing yaml - but can't use yaml library
        with open(f'{AMZ_CONFIG_DIR}/amz-config.yaml') as f:
            amz_repos = [
                re.search('- (.*)\n', x).group(1) for x in f.readlines() if re.search('- (.*)\n', x) is not None
            ]

        for repo in amz_repos:
            # Copy config files to root of repo: pre-commit, clang-format, yapf, cpplint, and pylint
            if os.path.exists(f'{repo}/amz.yaml'):
                copy_tree(f'{AMZ_DATA_DIR}/githooks/config/', repo)
    except:
        print('Error copying config files')
        sys.exit(1)
