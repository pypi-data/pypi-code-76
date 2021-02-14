# Copyright 2013-2019 The Meson development team

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This file contains the detection logic for miscellaneous external dependencies.

import functools
import os
import re
import shutil
import subprocess
from pathlib import Path

from ..mesonlib import OrderedSet, join_args
from .base import (
    DependencyException, DependencyMethods, ConfigToolDependency,
    PkgConfigDependency, factory_methods
)
import typing as T

if T.TYPE_CHECKING:
    from .base import Dependency
    from ..environment import Environment
    from ..mesonlib import MachineChoice


class HDF5PkgConfigDependency(PkgConfigDependency):

    """Handle brokenness in the HDF5 pkg-config files."""

    def __init__(self, name: str, environment: 'Environment', kwargs: T.Dict[str, T.Any], language: T.Optional[str] = None) -> None:
        language = language or 'c'
        if language not in {'c', 'cpp', 'fortran'}:
            raise DependencyException('Language {} is not supported with HDF5.'.format(language))

        super().__init__(name, environment, kwargs, language)
        if not self.is_found:
            return

        # some broken pkgconfig don't actually list the full path to the needed includes
        newinc = []  # type: T.List[str]
        for arg in self.compile_args:
            if arg.startswith('-I'):
                stem = 'static' if kwargs.get('static', False) else 'shared'
                if (Path(arg[2:]) / stem).is_dir():
                    newinc.append('-I' + str(Path(arg[2:]) / stem))
        self.compile_args += newinc

        link_args = []  # type: T.List[str]
        for larg in self.get_link_args():
            lpath = Path(larg)
            # some pkg-config hdf5.pc (e.g. Ubuntu) don't include the commonly-used HL HDF5 libraries,
            # so let's add them if they exist
            # additionally, some pkgconfig HDF5 HL files are malformed so let's be sure to find HL anyway
            if lpath.is_file():
                hl = []
                if language == 'cpp':
                    hl += ['_hl_cpp', '_cpp']
                elif language == 'fortran':
                    hl += ['_hl_fortran', 'hl_fortran', '_fortran']
                hl += ['_hl']  # C HL library, always needed

                suffix = '.' + lpath.name.split('.', 1)[1]  # in case of .dll.a
                for h in hl:
                    hlfn = lpath.parent / (lpath.name.split('.', 1)[0] + h + suffix)
                    if hlfn.is_file():
                        link_args.append(str(hlfn))
                # HDF5 C libs are required by other HDF5 languages
                link_args.append(larg)
            else:
                link_args.append(larg)

        self.link_args = link_args


class HDF5ConfigToolDependency(ConfigToolDependency):

    """Wrapper around hdf5 binary config tools."""

    version_arg = '-showconfig'

    def __init__(self, name: str, environment: 'Environment', kwargs: T.Dict[str, T.Any], language: T.Optional[str] = None) -> None:
        language = language or 'c'
        if language not in {'c', 'cpp', 'fortran'}:
            raise DependencyException('Language {} is not supported with HDF5.'.format(language))

        if language == 'c':
            cenv = 'CC'
            tools = ['h5cc']
        elif language == 'cpp':
            cenv = 'CXX'
            tools = ['h5c++']
        elif language == 'fortran':
            cenv = 'FC'
            tools = ['h5fc']
        else:
            raise DependencyException('How did you get here?')

        # We need this before we call super()
        for_machine = self.get_for_machine_from_kwargs(kwargs)

        nkwargs = kwargs.copy()
        nkwargs['tools'] = tools

        # Override the compiler that the config tools are going to use by
        # setting the environment variables that they use for the compiler and
        # linkers.
        compiler = environment.coredata.compilers[for_machine][language]
        try:
            os.environ['HDF5_{}'.format(cenv)] = join_args(compiler.get_exelist())
            os.environ['HDF5_{}LINKER'.format(cenv)] = join_args(compiler.get_linker_exelist())
            super().__init__(name, environment, nkwargs, language)
        finally:
            del os.environ['HDF5_{}'.format(cenv)]
            del os.environ['HDF5_{}LINKER'.format(cenv)]
        if not self.is_found:
            return

        args = self.get_config_value(['-show', '-noshlib' if kwargs.get('static', False) else '-shlib'], 'args')
        for arg in args[1:]:
            if arg.startswith(('-I', '-f', '-D')) or arg == '-pthread':
                self.compile_args.append(arg)
            elif arg.startswith(('-L', '-l', '-Wl')):
                self.link_args.append(arg)
            elif Path(arg).is_file():
                self.link_args.append(arg)

        # If the language is not C we need to add C as a subdependency
        if language != 'c':
            nkwargs = kwargs.copy()
            nkwargs['language'] = 'c'
            # I'm being too clever for mypy and pylint
            self.is_found = self._add_sub_dependency(hdf5_factory(environment, for_machine, nkwargs))  # type: ignore  # pylint: disable=no-value-for-parameter

    def _sanitize_version(self, ver: str) -> str:
        v = re.search(r'\s*HDF5 Version: (\d+\.\d+\.\d+)', ver)
        return v.group(1)


@factory_methods({DependencyMethods.PKGCONFIG, DependencyMethods.CONFIG_TOOL})
def hdf5_factory(env: 'Environment', for_machine: 'MachineChoice',
                 kwargs: T.Dict[str, T.Any], methods: T.List[DependencyMethods]) -> T.List[T.Callable[[], 'Dependency']]:
    language = kwargs.get('language')
    candidates = []  # type: T.List[T.Callable[[], Dependency]]

    if DependencyMethods.PKGCONFIG in methods:
        # Use an ordered set so that these remain the first tried pkg-config files
        pkgconfig_files = OrderedSet(['hdf5', 'hdf5-serial'])
        # FIXME: This won't honor pkg-config paths, and cross-native files
        PCEXE = shutil.which('pkg-config')
        if PCEXE:
            # some distros put hdf5-1.2.3.pc with version number in .pc filename.
            ret = subprocess.run([PCEXE, '--list-all'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                    universal_newlines=True)
            if ret.returncode == 0:
                for pkg in ret.stdout.split('\n'):
                    if pkg.startswith(('hdf5')):
                        pkgconfig_files.add(pkg.split(' ', 1)[0])

        for pkg in pkgconfig_files:
            candidates.append(functools.partial(HDF5PkgConfigDependency, pkg, env, kwargs, language))

    if DependencyMethods.CONFIG_TOOL in methods:
        candidates.append(functools.partial(HDF5ConfigToolDependency, 'hdf5', env, kwargs, language))

    return candidates
