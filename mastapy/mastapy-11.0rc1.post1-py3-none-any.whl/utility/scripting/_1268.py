'''_1268.py

ScriptingSetup
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy.utility import _1143
from mastapy._internal.python_net import python_net_import

_SCRIPTING_SETUP = python_net_import('SMT.MastaAPI.Utility.Scripting', 'ScriptingSetup')


__docformat__ = 'restructuredtext en'
__all__ = ('ScriptingSetup',)


class ScriptingSetup(_1143.PerMachineSettings):
    '''ScriptingSetup

    This is a mastapy class.
    '''

    TYPE = _SCRIPTING_SETUP

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ScriptingSetup.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def select_plug_in_directory(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SelectPlugInDirectory' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectPlugInDirectory

    @property
    def add_existing_net_solution(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'AddExistingNETSolution' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddExistingNETSolution

    @property
    def use_default_plug_in_directory(self) -> 'bool':
        '''bool: 'UseDefaultPlugInDirectory' is the original name of this property.'''

        return self.wrapped.UseDefaultPlugInDirectory

    @use_default_plug_in_directory.setter
    def use_default_plug_in_directory(self, value: 'bool'):
        self.wrapped.UseDefaultPlugInDirectory = bool(value) if value else False

    @property
    def select_net_solution_directory(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SelectNETSolutionDirectory' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectNETSolutionDirectory

    @property
    def use_default_net_solution_directory(self) -> 'bool':
        '''bool: 'UseDefaultNETSolutionDirectory' is the original name of this property.'''

        return self.wrapped.UseDefaultNETSolutionDirectory

    @use_default_net_solution_directory.setter
    def use_default_net_solution_directory(self, value: 'bool'):
        self.wrapped.UseDefaultNETSolutionDirectory = bool(value) if value else False

    @property
    def select_python_scripts_directory(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SelectPythonScriptsDirectory' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectPythonScriptsDirectory

    @property
    def use_default_python_scripts_directory(self) -> 'bool':
        '''bool: 'UseDefaultPythonScriptsDirectory' is the original name of this property.'''

        return self.wrapped.UseDefaultPythonScriptsDirectory

    @use_default_python_scripts_directory.setter
    def use_default_python_scripts_directory(self, value: 'bool'):
        self.wrapped.UseDefaultPythonScriptsDirectory = bool(value) if value else False

    @property
    def python_install_directory(self) -> 'str':
        '''str: 'PythonInstallDirectory' is the original name of this property.'''

        return self.wrapped.PythonInstallDirectory

    @python_install_directory.setter
    def python_install_directory(self, value: 'str'):
        self.wrapped.PythonInstallDirectory = str(value) if value else None

    @property
    def python_home_directory(self) -> 'str':
        '''str: 'PythonHomeDirectory' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PythonHomeDirectory

    @property
    def python_exe_path(self) -> 'str':
        '''str: 'PythonExePath' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PythonExePath

    @property
    def select_python_install_directory(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SelectPythonInstallDirectory' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectPythonInstallDirectory

    @property
    def run_scripts_in_separate_threads(self) -> 'bool':
        '''bool: 'RunScriptsInSeparateThreads' is the original name of this property.'''

        return self.wrapped.RunScriptsInSeparateThreads

    @run_scripts_in_separate_threads.setter
    def run_scripts_in_separate_threads(self, value: 'bool'):
        self.wrapped.RunScriptsInSeparateThreads = bool(value) if value else False
