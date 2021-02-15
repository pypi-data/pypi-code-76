"""
MKREXX - Library utility that leverage include statements in rexx files for the build process.

This program and the accompanying materials are made available under the terms of
The Apache-2.0 License which accompanies this distribution, and is available at
http://www.apache.org/licenses/LICENSE-2.0

SPDX-License-Identifier: Apache-2.0

Copyright (c) Mainframe Services Engineering (IBM GTS).

"""
import os
import configparser
import functools
import time
from decouple import config
from pathlib import Path
from .utilities import FileSystemManager
from .utilities import BG
from .utilities import LOG

PROG_NAME = "MkRexx"


def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        target_object = args[0]
        setattr(target_object, '_run_time', run_time)
        LOG.info(f'Build process completed in {BG.OKGREEN}{run_time:.3f}{BG.ENDC} seconds.')
        return value
    return wrapper_timer

class MakeRexx:

    def __init__(self, origin_path=None, lib_path=None, build_path=None, config_path=None):

        if not origin_path and not lib_path and not build_path:
            if config_path:
                self.config = configparser.ConfigParser()
                self.config.read(config_path)
                self.__read_config_from_config_file()
            else:
                self.__read_config_from_environment()
        else:
            self.origin_path = origin_path
            self.lib_path = lib_path
            self.build_path = build_path
        self.parse_paths()

    def __read_config_from_config_file(self):
        """Retrieve configuration values from config file."""
        LOG.info(f'Retrieving data from config file')
        self.lib_path = self.config.get('REXX_LIBRARY', 'PATH')
        self.origin_path = self.config.get('REXX_ORIGIN', 'PATH')
        self.build_path = self.config.get('REXX_BUILD', 'PATH')

    def __read_config_from_environment(self):
        LOG.info(f'Retrieving config data from environment')
        self.lib_path = config('REXX_LIB_PATH')
        self.origin_path = config('REXX_ORIGIN_PATH')
        self.build_path = config('REXX_BUILD_PATH')

    @timer
    def build(self):
        """Initiate the build process for MKREXX."""
        LOG.info(f'{BG.OKBLUE}Initializing build process..{BG.ENDC}')
        for origin_file_name, origin_file_object in self.origin_files.items():
            self.append_build_time_header(origin_file_object)
            self.make_include(origin_file_object)
        self.parse_build_files()

    def parse_paths(self):
        """Parse REXX contents for all paths of the configuration."""
        self.files_manager = FileSystemManager()
        self.library_files = self.files_manager.load_files(self.lib_path)
        self.origin_files = self.files_manager.load_files(self.origin_path)

    def parse_build_files(self):
        self.build_files = self.files_manager.load_files(self.build_path)

    def append_build_time_header(self, file_object):
        """Append timestamp of the build to the header of the REXX file."""
        LOG.debug(f'Appending build header for {file_object.file_name}')
        build_time_header = f'MKREXX Build: {time.asctime()}'
        file_object.code.append_comment(build_time_header, index=1)

    def make_include(self, file_object):
        """Process the include statements during the build process."""
        LOG.info(f'Make include for "{file_object.file_name}"')
        build_file_name = f'{file_object.file_name}'
        self.current_build_path = self.__generate_current_build_path(file_object)
        self.setup_build_file(file_object)
        for include_statement in file_object.code.include_statements:
            self.handle_include_statements(include_statement)

    def __generate_current_build_path(self, file_object):
        file_dir = os.path.dirname(file_object.file_path)
        # Quick hack in case the origin file is located in a subdir
        new_path = file_dir.replace(self.origin_path.strip(os.path.sep),
                                    self.build_path.strip(os.path.sep))
        try:
            Path(new_path).mkdir(parents=True, exist_ok=True)
        except FileExistsError:
            pass
        build_path = os.path.join(new_path, file_object.file_name)
        return build_path


    def setup_build_file(self, setup_file_object):
        """Setup build process by appending original content of the file first."""
        with open(self.current_build_path, 'w') as build_file:
            build_file.writelines("\n".join(setup_file_object.code.records))

    def handle_include_statements(self, include_statement):
        """Add the include statements to the current build file."""
        with open(self.current_build_path, 'a') as build_file:
            library_file_object = self.library_files[include_statement.file_name]
            build_file.write('\n\n')
            build_file.write(f'/* {PROG_NAME}: Including routines from {include_statement.file_name} */\n')
            if include_statement.routines:
                LOG.debug(f'+ from <{include_statement.file_name}> including routines {include_statement.routines}')
                for routine in include_statement.routines:
                    routine_contents = library_file_object.code.get_routine_contents(routine)
                    build_file.writelines("\n".join(routine_contents))
                    build_file.write('\n')
            elif include_statement.negative_routines:
                LOG.debug(f'+ from <{include_statement.file_name}> including all routines except {include_statement.negative_routines}')
                for routine_name, routine_object in library_file_object.code.rexx_routines.items():
                    if routine_name not in include_statement.negative_routines:
                        routine_contents = library_file_object.code.get_routine_contents(routine_name)
                        build_file.writelines("\n".join(routine_contents))
                        build_file.write("\n")
            else:
                LOG.debug(f'+ including <{include_statement.file_name}> from lib')
                build_file.writelines(library_file_object.file_contents)