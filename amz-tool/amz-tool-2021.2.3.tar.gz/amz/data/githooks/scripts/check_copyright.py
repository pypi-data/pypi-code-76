#!/usr/bin/env python3
'''
Assumes incoming files to be python or C/C++,
filtered from pre-commit framework
'''

import os
import sys
import re
from identify import identify

file_list = sys.argv[1:]

# Exit if no files given
if not file_list:
    print("No files given!")
    sys.exit(0)


def check_file(filepath: str, comment_symbol: str):
    with open(filepath, 'r') as f:
        # Search for beginning of disclaimer
        for i, line in enumerate(f):
            line = line.replace(comment_symbol, '').strip()
            if line == 'AMZ Driverless Project':
                break
            # Give up after 10 lines:
            if i == 10:
                return False
        # Empty line
        if next(f).replace(comment_symbol, '').strip():
            return False
        # Copyright line
        line = next(f).replace(comment_symbol, '').strip()
        if re.compile(r'Copyright \(c\) 20(1|2)\d(-20(1|2)\d)? Authors:').match(line) is None:
            return False
        # List of authors
        for i, line in enumerate(f):
            line = line.replace(comment_symbol, '').strip()
            # Reached end of the list
            if not line:
                if i == 0:
                    return False
                break
            if re.compile(r'- .+?(?=<)<.+?(?=@)@.+?(?=>)>').match(line) is None:
                return False
        # The next lines need to match literally
        if next(f).replace(comment_symbol, '').strip() != 'All rights reserved.':
            return False
        if next(f).replace(comment_symbol, '').strip():
            return False
        line = next(f).replace(comment_symbol, '').strip()
        if line != 'Unauthorized copying of this file, via any medium is strictly prohibited':
            return False
        if next(f).replace(comment_symbol, '').strip() != 'Proprietary and confidential':
            return False
    return True


failed_files = []
error_files = []

# Check all given files
for file in file_list:
    # Skip empty files like __init__.py
    if os.stat(file).st_size == 0:
        continue
    # Use tag indentification as being done in pre-commit
    tags = identify.tags_from_path(file)
    if 'python' in tags:
        if not check_file(file, '#'):
            failed_files.append(file)
    elif 'c++' in tags:
        if not check_file(file, '*'):
            failed_files.append(file)
    else:
        error_files.append(file)

COLLECTED_EXIT = 0
COLLECTED_OUTPUT = ''

# Print error messages
if failed_files:
    COLLECTED_EXIT += 1
    COLLECTED_OUTPUT += '\n----------\033[31m Did not find proper AMZ copyright disclaimers. \033[0m\n'
    COLLECTED_OUTPUT += '\nThe following files failed:\n'
    COLLECTED_OUTPUT += '\t' + '\n\t'.join(failed_files)
if error_files:
    COLLECTED_EXIT += 1
    COLLECTED_OUTPUT += '\n----------\033[31m The following files could not be indentified as Python or C/C++ code'
    COLLECTED_OUTPUT += ' \033[0m\n'
    COLLECTED_OUTPUT += '\nThe following files failed:\n'
    COLLECTED_OUTPUT += '\t' + '\n\t'.join(error_files)

COLLECTED_OUTPUT += '\n----------'

if COLLECTED_EXIT != 0:
    print(COLLECTED_OUTPUT)
sys.exit(COLLECTED_EXIT)
