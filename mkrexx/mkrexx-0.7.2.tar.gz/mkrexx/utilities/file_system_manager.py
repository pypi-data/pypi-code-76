"""
MKREXX - Library utility that leverage include statements in rexx files for the build process.

This program and the accompanying materials are made available under the terms of
The Apache-2.0 License which accompanies this distribution, and is available at
http://www.apache.org/licenses/LICENSE-2.0

SPDX-License-Identifier: Apache-2.0

Copyright (c) Mainframe Services Engineering (IBM GTS).

"""

import os
from .background_colors import BG
from .logger import LOG
from pyrexx import RexxFile

REXX_FILE_EXTENSIONS = ['rex', 'rexx']


class FileSystemManager:
    """FileSystemManager class."""

    def load_files(self, input_path):
        """Load files from given input path to a given dictionary."""
        temp_dict = {}
        LOG.info(f'Reading files from path {input_path}')

        try:
            for current_path, subdir, files in os.walk(input_path):
                for file_name in files:
                    if self.file_has_rexx_extension(file_name):
                        file_base_name = file_name.split(".")[0]
                        LOG.debug(f'Analysing {file_name}')
                        file_path = os.path.abspath(os.path.join(current_path, file_name))
                        temp_dict[file_base_name] = RexxFile(file_name, file_path)
                    else:
                        LOG.debug(f'{file_name} is does\'t have REXX source code extension')
        except FileNotFoundError as error:
            LOG.warn(f'Error while trying to read from file in inputh path "{input_path}": {error}')
        return temp_dict

    def file_has_rexx_extension(self, file_name):
        """Return true in case file ends with .rex or .rexx ."""
        extension = file_name.split(".")[1].lower()
        return extension in REXX_FILE_EXTENSIONS
