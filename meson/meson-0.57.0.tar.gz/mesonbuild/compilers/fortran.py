# Copyright 2012-2017 The Meson development team

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path
import typing as T
import subprocess, os

from .. import coredata
from .compilers import (
    clike_debug_args,
    Compiler,
)
from .mixins.clike import CLikeCompiler
from .mixins.gnu import (
    GnuCompiler, gnulike_buildtype_args, gnu_optimization_args,
)
from .mixins.intel import IntelGnuLikeCompiler, IntelVisualStudioLikeCompiler
from .mixins.clang import ClangCompiler
from .mixins.elbrus import ElbrusCompiler
from .mixins.pgi import PGICompiler

from mesonbuild.mesonlib import (
    version_compare, EnvironmentException, MesonException, MachineChoice,
    LibType, OptionKey,
)

if T.TYPE_CHECKING:
    from ..coredata import KeyedOptionDictType
    from ..dependencies import Dependency, ExternalProgram
    from ..envconfig import MachineInfo
    from ..environment import Environment
    from ..linkers import DynamicLinker


class FortranCompiler(CLikeCompiler, Compiler):

    language = 'fortran'

    def __init__(self, exelist: T.List[str], version: str, for_machine: MachineChoice, is_cross: bool,
                 info: 'MachineInfo', exe_wrapper: T.Optional['ExternalProgram'] = None,
                 linker: T.Optional['DynamicLinker'] = None,
                 full_version: T.Optional[str] = None):
        Compiler.__init__(self, exelist, version, for_machine, info,
                          is_cross=is_cross, full_version=full_version, linker=linker)
        CLikeCompiler.__init__(self, exe_wrapper)

    def has_function(self, funcname: str, prefix: str, env: 'Environment', *,
                     extra_args: T.Optional[T.List[str]] = None,
                     dependencies: T.Optional[T.List['Dependency']] = None) -> T.Tuple[bool, bool]:
        raise MesonException('Fortran does not have "has_function" capability.\n'
                             'It is better to test if a Fortran capability is working like:\n\n'
                             "meson.get_compiler('fortran').links('block; end block; end program')\n\n"
                             'that example is to see if the compiler has Fortran 2008 Block element.')

    def sanity_check(self, work_dir_: str, environment: 'Environment') -> None:
        work_dir = Path(work_dir_)
        source_name = work_dir / 'sanitycheckf.f90'
        binary_name = work_dir / 'sanitycheckf'
        if binary_name.is_file():
            binary_name.unlink()

        source_name.write_text('print *, "Fortran compilation is working."; end')

        extra_flags: T.List[str] = []
        extra_flags += environment.coredata.get_external_args(self.for_machine, self.language)
        extra_flags += environment.coredata.get_external_link_args(self.for_machine, self.language)
        extra_flags += self.get_always_args()
        # %% build the test executable "sanitycheckf"
        # cwd=work_dir is necessary on Windows especially for Intel compilers to avoid error: cannot write on sanitycheckf.obj
        # this is a defect with how Windows handles files and ifort's object file-writing behavior vis concurrent ProcessPoolExecutor.
        # This simple workaround solves the issue.
        # FIXME: cwd=str(work_dir) is for Python 3.5 on Windows, when 3.5 is deprcated, this can become cwd=work_dir
        returncode = subprocess.run(self.exelist + extra_flags + [str(source_name), '-o', str(binary_name)],
                                    cwd=str(work_dir)).returncode
        if returncode != 0:
            raise EnvironmentException('Compiler %s can not compile programs.' % self.name_string())
        if self.is_cross:
            if self.exe_wrapper is None:
                # Can't check if the binaries run so we have to assume they do
                return
            cmdlist = self.exe_wrapper.get_command() + [str(binary_name)]
        else:
            cmdlist = [str(binary_name)]
        # %% Run the test executable
        try:
            returncode = subprocess.run(cmdlist, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
            if returncode != 0:
                raise EnvironmentException('Executables created by Fortran compiler %s are not runnable.' % self.name_string())
        except OSError:
            raise EnvironmentException('Executables created by Fortran compiler %s are not runnable.' % self.name_string())

    def get_buildtype_args(self, buildtype: str) -> T.List[str]:
        return gnulike_buildtype_args[buildtype]

    def get_optimization_args(self, optimization_level: str) -> T.List[str]:
        return gnu_optimization_args[optimization_level]

    def get_debug_args(self, is_debug: bool) -> T.List[str]:
        return clike_debug_args[is_debug]

    def get_preprocess_only_args(self) -> T.List[str]:
        return ['-cpp'] + super().get_preprocess_only_args()

    def get_module_incdir_args(self) -> T.Tuple[str, ...]:
        return ('-I', )

    def get_module_outdir_args(self, path: str) -> T.List[str]:
        return ['-module', path]

    def compute_parameters_with_absolute_paths(self, parameter_list: T.List[str],
                                               build_dir: str) -> T.List[str]:
        for idx, i in enumerate(parameter_list):
            if i[:2] == '-I' or i[:2] == '-L':
                parameter_list[idx] = i[:2] + os.path.normpath(os.path.join(build_dir, i[2:]))

        return parameter_list

    def module_name_to_filename(self, module_name: str) -> str:
        if '_' in module_name:  # submodule
            s = module_name.lower()
            if self.id in ('gcc', 'intel', 'intel-cl'):
                filename = s.replace('_', '@') + '.smod'
            elif self.id in ('pgi', 'flang'):
                filename = s.replace('_', '-') + '.mod'
            else:
                filename = s + '.mod'
        else:  # module
            filename = module_name.lower() + '.mod'

        return filename

    def find_library(self, libname: str, env: 'Environment', extra_dirs: T.List[str],
                     libtype: LibType = LibType.PREFER_SHARED) -> T.Optional[T.List[str]]:
        code = 'stop; end program'
        return self._find_library_impl(libname, env, extra_dirs, code, libtype)

    def has_multi_arguments(self, args: T.List[str], env: 'Environment') -> T.Tuple[bool, bool]:
        return self._has_multi_arguments(args, env, 'stop; end program')

    def has_multi_link_arguments(self, args: T.List[str], env: 'Environment') -> T.Tuple[bool, bool]:
        return self._has_multi_link_arguments(args, env, 'stop; end program')

    def get_options(self) -> 'KeyedOptionDictType':
        opts = super().get_options()
        key = OptionKey('std', machine=self.for_machine, lang=self.language)
        opts.update({
            key: coredata.UserComboOption(
                'Fortran language standard to use',
                ['none'],
                'none',
            ),
        })
        return opts


class GnuFortranCompiler(GnuCompiler, FortranCompiler):

    def __init__(self, exelist: T.List[str], version: str, for_machine: MachineChoice, is_cross: bool,
                 info: 'MachineInfo', exe_wrapper: T.Optional['ExternalProgram'] = None,
                 defines: T.Optional[T.Dict[str, str]] = None,
                 linker: T.Optional['DynamicLinker'] = None,
                 full_version: T.Optional[str] = None):
        FortranCompiler.__init__(self, exelist, version, for_machine,
                                 is_cross, info, exe_wrapper, linker=linker,
                                 full_version=full_version)
        GnuCompiler.__init__(self, defines)
        default_warn_args = ['-Wall']
        self.warn_args = {'0': [],
                          '1': default_warn_args,
                          '2': default_warn_args + ['-Wextra'],
                          '3': default_warn_args + ['-Wextra', '-Wpedantic', '-fimplicit-none']}

    def get_options(self) -> 'KeyedOptionDictType':
        opts = FortranCompiler.get_options(self)
        fortran_stds = ['legacy', 'f95', 'f2003']
        if version_compare(self.version, '>=4.4.0'):
            fortran_stds += ['f2008']
        if version_compare(self.version, '>=8.0.0'):
            fortran_stds += ['f2018']
        key = OptionKey('std', machine=self.for_machine, lang=self.language)
        opts[key].choices = ['none'] + fortran_stds
        return opts

    def get_option_compile_args(self, options: 'KeyedOptionDictType') -> T.List[str]:
        args = []
        key = OptionKey('std', machine=self.for_machine, lang=self.language)
        std = options[key]
        if std.value != 'none':
            args.append('-std=' + std.value)
        return args

    def get_dependency_gen_args(self, outtarget: str, outfile: str) -> T.List[str]:
        # Disabled until this is fixed:
        # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=62162
        # return ['-cpp', '-MD', '-MQ', outtarget]
        return []

    def get_module_outdir_args(self, path: str) -> T.List[str]:
        return ['-J' + path]

    def language_stdlib_only_link_flags(self) -> T.List[str]:
        return ['-lgfortran', '-lm']

    def has_header(self, hname: str, prefix: str, env: 'Environment', *,
                   extra_args: T.Optional[T.List[str]] = None,
                   dependencies: T.Optional[T.List['Dependency']] = None,
                   disable_cache: bool = False) -> T.Tuple[bool, bool]:
        '''
        Derived from mixins/clike.py:has_header, but without C-style usage of
        __has_include which breaks with GCC-Fortran 10:
        https://github.com/mesonbuild/meson/issues/7017
        '''
        fargs = {'prefix': prefix, 'header': hname}
        code = '{prefix}\n#include <{header}>'
        return self.compiles(code.format(**fargs), env, extra_args=extra_args,
                             dependencies=dependencies, mode='preprocess', disable_cache=disable_cache)


class ElbrusFortranCompiler(GnuFortranCompiler, ElbrusCompiler):
    def __init__(self, exelist: T.List[str], version: str, for_machine: MachineChoice, is_cross: bool,
                 info: 'MachineInfo', exe_wrapper: T.Optional['ExternalProgram'] = None,
                 defines: T.Optional[T.Dict[str, str]] = None,
                 linker: T.Optional['DynamicLinker'] = None,
                 full_version: T.Optional[str] = None):
        GnuFortranCompiler.__init__(self, exelist, version, for_machine, is_cross,
                                    info, exe_wrapper, defines=defines,
                                    linker=linker, full_version=full_version)
        ElbrusCompiler.__init__(self)

class G95FortranCompiler(FortranCompiler):

    LINKER_PREFIX = '-Wl,'

    def __init__(self, exelist: T.List[str], version: str, for_machine: MachineChoice, is_cross: bool,
                 info: 'MachineInfo', exe_wrapper: T.Optional['ExternalProgram'] = None,
                 linker: T.Optional['DynamicLinker'] = None,
                 full_version: T.Optional[str] = None):
        FortranCompiler.__init__(self, exelist, version, for_machine,
                                 is_cross, info, exe_wrapper, linker=linker,
                                 full_version=full_version)
        self.id = 'g95'
        default_warn_args = ['-Wall']
        self.warn_args = {'0': [],
                          '1': default_warn_args,
                          '2': default_warn_args + ['-Wextra'],
                          '3': default_warn_args + ['-Wextra', '-pedantic']}

    def get_module_outdir_args(self, path: str) -> T.List[str]:
        return ['-fmod=' + path]

    def get_no_warn_args(self) -> T.List[str]:
        # FIXME: Confirm that there's no compiler option to disable all warnings
        return []


class SunFortranCompiler(FortranCompiler):

    LINKER_PREFIX = '-Wl,'

    def __init__(self, exelist: T.List[str], version: str, for_machine: MachineChoice, is_cross: bool,
                 info: 'MachineInfo', exe_wrapper: T.Optional['ExternalProgram'] = None,
                 linker: T.Optional['DynamicLinker'] = None,
                 full_version: T.Optional[str] = None):
        FortranCompiler.__init__(self, exelist, version, for_machine,
                                 is_cross, info, exe_wrapper, linker=linker,
                                 full_version=full_version)
        self.id = 'sun'

    def get_dependency_gen_args(self, outtarget: str, outfile: str) -> T.List[str]:
        return ['-fpp']

    def get_always_args(self) -> T.List[str]:
        return []

    def get_warn_args(self, level: str) -> T.List[str]:
        return []

    def get_module_incdir_args(self) -> T.Tuple[str, ...]:
        return ('-M', )

    def get_module_outdir_args(self, path: str) -> T.List[str]:
        return ['-moddir=' + path]

    def openmp_flags(self) -> T.List[str]:
        return ['-xopenmp']


class IntelFortranCompiler(IntelGnuLikeCompiler, FortranCompiler):

    file_suffixes = ('f90', 'f', 'for', 'ftn', 'fpp', )

    def __init__(self, exelist: T.List[str], version: str, for_machine: MachineChoice, is_cross: bool,
                 info: 'MachineInfo', exe_wrapper: T.Optional['ExternalProgram'] = None,
                 linker: T.Optional['DynamicLinker'] = None,
                 full_version: T.Optional[str] = None):
        FortranCompiler.__init__(self, exelist, version, for_machine,
                                 is_cross, info, exe_wrapper, linker=linker,
                                 full_version=full_version)
        # FIXME: Add support for OS X and Windows in detect_fortran_compiler so
        # we are sent the type of compiler
        IntelGnuLikeCompiler.__init__(self)
        self.id = 'intel'
        default_warn_args = ['-warn', 'general', '-warn', 'truncated_source']
        self.warn_args = {'0': [],
                          '1': default_warn_args,
                          '2': default_warn_args + ['-warn', 'unused'],
                          '3': ['-warn', 'all']}

    def get_options(self) -> 'KeyedOptionDictType':
        opts = FortranCompiler.get_options(self)
        key = OptionKey('std', machine=self.for_machine, lang=self.language)
        opts[key].choices = ['none', 'legacy', 'f95', 'f2003', 'f2008', 'f2018']
        return opts

    def get_option_compile_args(self, options: 'KeyedOptionDictType') -> T.List[str]:
        args = []
        key = OptionKey('std', machine=self.for_machine, lang=self.language)
        std = options[key]
        stds = {'legacy': 'none', 'f95': 'f95', 'f2003': 'f03', 'f2008': 'f08', 'f2018': 'f18'}
        if std.value != 'none':
            args.append('-stand=' + stds[std.value])
        return args

    def get_preprocess_only_args(self) -> T.List[str]:
        return ['-cpp', '-EP']

    def get_always_args(self) -> T.List[str]:
        """Ifort doesn't have -pipe."""
        val = super().get_always_args()
        val.remove('-pipe')
        return val

    def language_stdlib_only_link_flags(self) -> T.List[str]:
        return ['-lifcore', '-limf']

    def get_dependency_gen_args(self, outtarget: str, outfile: str) -> T.List[str]:
        return ['-gen-dep=' + outtarget, '-gen-depformat=make']


class IntelClFortranCompiler(IntelVisualStudioLikeCompiler, FortranCompiler):

    file_suffixes = ('f90', 'f', 'for', 'ftn', 'fpp', )
    always_args = ['/nologo']

    def __init__(self, exelist: T.List[str], version: str, for_machine: MachineChoice,
                 is_cross: bool, info: 'MachineInfo', target: str,
                 exe_wrapper: T.Optional['ExternalProgram'] = None,
                 linker: T.Optional['DynamicLinker'] = None,
                 full_version: T.Optional[str] = None):
        FortranCompiler.__init__(self, exelist, version, for_machine,
                                 is_cross, info, exe_wrapper, linker=linker,
                                 full_version=full_version)
        IntelVisualStudioLikeCompiler.__init__(self, target)

        default_warn_args = ['/warn:general', '/warn:truncated_source']
        self.warn_args = {'0': [],
                          '1': default_warn_args,
                          '2': default_warn_args + ['/warn:unused'],
                          '3': ['/warn:all']}

    def get_options(self) -> 'KeyedOptionDictType':
        opts = FortranCompiler.get_options(self)
        key = OptionKey('std', machine=self.for_machine, lang=self.language)
        opts[key].choices = ['none', 'legacy', 'f95', 'f2003', 'f2008', 'f2018']
        return opts

    def get_option_compile_args(self, options: 'KeyedOptionDictType') -> T.List[str]:
        args = []
        key = OptionKey('std', machine=self.for_machine, lang=self.language)
        std = options[key]
        stds = {'legacy': 'none', 'f95': 'f95', 'f2003': 'f03', 'f2008': 'f08', 'f2018': 'f18'}
        if std.value != 'none':
            args.append('/stand:' + stds[std.value])
        return args

    def get_module_outdir_args(self, path: str) -> T.List[str]:
        return ['/module:' + path]


class PathScaleFortranCompiler(FortranCompiler):

    def __init__(self, exelist: T.List[str], version: str, for_machine: MachineChoice, is_cross: bool,
                 info: 'MachineInfo', exe_wrapper: T.Optional['ExternalProgram'] = None,
                 linker: T.Optional['DynamicLinker'] = None,
                 full_version: T.Optional[str] = None):
        FortranCompiler.__init__(self, exelist, version, for_machine,
                                 is_cross, info, exe_wrapper, linker=linker,
                                 full_version=full_version)
        self.id = 'pathscale'
        default_warn_args = ['-fullwarn']
        self.warn_args = {'0': [],
                          '1': default_warn_args,
                          '2': default_warn_args,
                          '3': default_warn_args}

    def openmp_flags(self) -> T.List[str]:
        return ['-mp']


class PGIFortranCompiler(PGICompiler, FortranCompiler):

    def __init__(self, exelist: T.List[str], version: str, for_machine: MachineChoice, is_cross: bool,
                 info: 'MachineInfo', exe_wrapper: T.Optional['ExternalProgram'] = None,
                 linker: T.Optional['DynamicLinker'] = None,
                 full_version: T.Optional[str] = None):
        FortranCompiler.__init__(self, exelist, version, for_machine,
                                 is_cross, info, exe_wrapper, linker=linker,
                                 full_version=full_version)
        PGICompiler.__init__(self)

        default_warn_args = ['-Minform=inform']
        self.warn_args = {'0': [],
                          '1': default_warn_args,
                          '2': default_warn_args,
                          '3': default_warn_args + ['-Mdclchk']}

    def language_stdlib_only_link_flags(self) -> T.List[str]:
        return ['-lpgf90rtl', '-lpgf90', '-lpgf90_rpm1', '-lpgf902',
                '-lpgf90rtl', '-lpgftnrtl', '-lrt']


class NvidiaHPC_FortranCompiler(PGICompiler, FortranCompiler):

    def __init__(self, exelist: T.List[str], version: str, for_machine: MachineChoice, is_cross: bool,
                 info: 'MachineInfo', exe_wrapper: T.Optional['ExternalProgram'] = None,
                 linker: T.Optional['DynamicLinker'] = None,
                 full_version: T.Optional[str] = None):
        FortranCompiler.__init__(self, exelist, version, for_machine,
                                 is_cross, info, exe_wrapper, linker=linker,
                                 full_version=full_version)
        PGICompiler.__init__(self)

        self.id = 'nvidia_hpc'
        default_warn_args = ['-Minform=inform']
        self.warn_args = {'0': [],
                          '1': default_warn_args,
                          '2': default_warn_args,
                          '3': default_warn_args + ['-Mdclchk']}


class FlangFortranCompiler(ClangCompiler, FortranCompiler):

    def __init__(self, exelist: T.List[str], version: str, for_machine: MachineChoice, is_cross: bool,
                 info: 'MachineInfo', exe_wrapper: T.Optional['ExternalProgram'] = None,
                 linker: T.Optional['DynamicLinker'] = None,
                 full_version: T.Optional[str] = None):
        FortranCompiler.__init__(self, exelist, version, for_machine,
                                 is_cross, info, exe_wrapper, linker=linker,
                                 full_version=full_version)
        ClangCompiler.__init__(self, {})
        self.id = 'flang'
        default_warn_args = ['-Minform=inform']
        self.warn_args = {'0': [],
                          '1': default_warn_args,
                          '2': default_warn_args,
                          '3': default_warn_args}

    def language_stdlib_only_link_flags(self) -> T.List[str]:
        return ['-lflang', '-lpgmath']

class Open64FortranCompiler(FortranCompiler):

    def __init__(self, exelist: T.List[str], version: str, for_machine: MachineChoice, is_cross: bool,
                 info: 'MachineInfo', exe_wrapper: T.Optional['ExternalProgram'] = None,
                 linker: T.Optional['DynamicLinker'] = None,
                 full_version: T.Optional[str] = None):
        FortranCompiler.__init__(self, exelist, version, for_machine,
                                 is_cross, info, exe_wrapper, linker=linker,
                                 full_version=full_version)
        self.id = 'open64'
        default_warn_args = ['-fullwarn']
        self.warn_args = {'0': [],
                          '1': default_warn_args,
                          '2': default_warn_args,
                          '3': default_warn_args}

    def openmp_flags(self) -> T.List[str]:
        return ['-mp']


class NAGFortranCompiler(FortranCompiler):

    def __init__(self, exelist: T.List[str], version: str, for_machine: MachineChoice, is_cross: bool,
                 info: 'MachineInfo', exe_wrapper: T.Optional['ExternalProgram'] = None,
                 linker: T.Optional['DynamicLinker'] = None,
                 full_version: T.Optional[str] = None):
        FortranCompiler.__init__(self, exelist, version, for_machine,
                                 is_cross, info, exe_wrapper, linker=linker,
                                 full_version=full_version)
        self.id = 'nagfor'

    def get_warn_args(self, level: str) -> T.List[str]:
        return []

    def get_module_outdir_args(self, path: str) -> T.List[str]:
        return ['-mdir', path]

    def openmp_flags(self) -> T.List[str]:
        return ['-openmp']
