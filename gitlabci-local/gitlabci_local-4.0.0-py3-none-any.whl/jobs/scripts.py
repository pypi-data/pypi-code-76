#!/usr/bin/env python3

# Standard libraries
from pathlib import Path
from sys import exc_info

# Components
from ..types.files import Files
from ..types.paths import Paths

# Scripts class
class Scripts:

    # Constants
    __SEPARATOR = '\n'

    # Members
    __file = None
    __target = None

    # Constructor
    def __init__(self, paths, prefix='.tmp.'):

        # Variables
        error = ''

        # Prepare members
        self.__file = None
        self.__target = None

        # Iterate through paths
        for path in paths:

            # Prepare temporary script
            try:
                self.__file = Files.temp(path=path, prefix=prefix)
                if isinstance(paths, dict) and paths[path]:
                    self.__target = Paths.get(
                        Path(paths[path]) / Path(self.__file.name).name)
                break
            except PermissionError:
                error = str(exc_info()[1])

        # Failed temporary script
        if not self.__file:
            raise PermissionError(error)

    # Configure
    def configure(self, errors=True, verbose=True):

        # Write shebang
        self.write('set -%s%s' % ('e' if errors else '', 'x' if verbose else ''))

    # Close
    def close(self):

        # Flush file
        self.flush()

        # Close file
        self.__file.close()

    # Flush
    def flush(self):

        # Flush file
        self.__file.flush()

    # Name
    def name(self):

        # Result
        return self.__file.name

    # Shebang
    def shebang(self):

        # Write shebang
        self.write('#!/bin/sh')

    # Subgroup start
    def subgroup_start(self):

        # Write subgroup start
        self.write('{')

    # Subgroup stop
    def subgroup_stop(self):

        # Write subgroup stop
        self.write('}')

    # Subshell start
    def subshell_start(self):

        # Write subshell start
        self.write('(')

    # Subshell stop
    def subshell_stop(self):

        # Write subshell stop
        self.write(') 2>&1')

    # Target
    def target(self):

        # Result
        return self.__target

    # Write
    def write(self, line=''):

        # Write line
        self.__file.write(line)
        self.__file.write(self.__SEPARATOR)

    # Write lines
    def writelines(self, lines):

        # Write line
        self.__file.write(self.__SEPARATOR.join(lines))
        self.__file.write(self.__SEPARATOR)
