#!/usr/bin/env python3
'''
Run appropriate linter on python files
Assumes incoming files to be python,
filtered from pre-commit framework
'''

import os
import sys
import subprocess as sp

file_list = sys.argv[1:]

# Exit if no files given
if not file_list:
    print("No files given!")
    sys.exit(0)

py2_files = []
py3_files = []
err_files = []

# Classify files into python2, py3 and non-shebanged files
for file in file_list:
    # Skip empty files like __init__.py
    if os.stat(file).st_size == 0:
        continue
    with open(file) as f:
        fl = f.readlines()[0]
        if "python2" in fl:
            py2_files.append(file)
        elif "python3" in fl:
            py3_files.append(file)
        else:
            err_files.append(file)

COLLECTED_EXIT = 0
COLLECTED_OUTPUT = ''

# Lint Py2 files
if py2_files:
    p = sp.run(f"python2 -m pylint {' '.join(py2_files)}", shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    COLLECTED_EXIT += p.returncode
    if p.returncode != 0:
        COLLECTED_OUTPUT += '\n----------\033[31m Pylint on Py2 Files \033[0m\n'
        COLLECTED_OUTPUT += p.stdout.decode()

# Lint Py3 files
if py3_files:
    # for file in py3_files:
    p = sp.run(f"python3 -m pylint {' '.join(py3_files)}", shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    COLLECTED_EXIT += p.returncode
    if p.returncode != 0:
        COLLECTED_OUTPUT += '\n----------\033[31m Pylint on Py3 Files \033[0m\n'
        COLLECTED_OUTPUT += p.stdout.decode()

# Finally deal with non-shebanged code
if err_files:
    COLLECTED_EXIT += 1
    COLLECTED_OUTPUT += '\n----------\033[31m Some Error Files \033[0m\n'
    COLLECTED_OUTPUT += "The following files possibly do not contain the right shebangs! \nDid not run pylint on:\n"
    COLLECTED_OUTPUT += '\t' + '\n\t'.join(err_files)
    COLLECTED_OUTPUT += '\n'

COLLECTED_OUTPUT += "----------"

if COLLECTED_EXIT != 0:
    print(COLLECTED_OUTPUT)
sys.exit(COLLECTED_EXIT)
