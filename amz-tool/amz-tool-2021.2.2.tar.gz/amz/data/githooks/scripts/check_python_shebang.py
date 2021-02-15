#!/usr/bin/env python3
'''
Assumes incoming files to be python,
filtered from pre-commit framework
'''

import os
import sys
import re

file_list = sys.argv[1:]

# Exit if no files given
if not file_list:
    print("No files given!")
    sys.exit(0)

failed_files = []

# Check all given files
for file in file_list:
    # Skip empty files like __init__.py
    if os.stat(file).st_size == 0:
        continue
    with open(file, 'r') as f:
        line = next(f).strip()
        if re.compile(r'#!\/usr\/bin\/env python(2|3)').match(line) is None:
            failed_files.append(file)

COLLECTED_EXIT = 0
COLLECTED_OUTPUT = ''

# Print error messages
if failed_files:
    COLLECTED_EXIT += 1
    COLLECTED_OUTPUT += '\n----------\033[31m Did not find clear python shebangs. \033[0m\n'
    COLLECTED_OUTPUT += 'Valid options are:\n#!/usr/bin/env python2\n#!/usr/bin/env python3\n'
    COLLECTED_OUTPUT += '\nThe following files failed:\n'
    COLLECTED_OUTPUT += '\t' + '\n\t'.join(failed_files)
    COLLECTED_OUTPUT += '\n----------'

if COLLECTED_EXIT != 0:
    print(COLLECTED_OUTPUT)
sys.exit(COLLECTED_EXIT)
