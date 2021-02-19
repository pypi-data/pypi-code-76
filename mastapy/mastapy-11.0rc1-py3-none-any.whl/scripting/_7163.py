'''_7163.py

ApiVersioning
'''


from typing import Iterable

from mastapy.scripting import _7156
from mastapy._internal import constructor, conversion
from mastapy._internal.python_net import python_net_import

_API_VERSIONING = python_net_import('SMT.MastaAPIUtility.Scripting', 'ApiVersioning')


__docformat__ = 'restructuredtext en'
__all__ = ('ApiVersioning',)


class ApiVersioning:
    '''ApiVersioning

    This is a mastapy class.
    '''

    TYPE = _API_VERSIONING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ApiVersioning.TYPE'):
        self.wrapped = instance_to_wrap

    @staticmethod
    def get_available_api_versions(folder: 'str') -> 'Iterable[_7156.ApiVersion]':
        ''' 'GetAvailableApiVersions' is the original name of this method.

        Args:
            folder (str)

        Returns:
            Iterable[mastapy.scripting.ApiVersion]
        '''

        folder = str(folder)
        return conversion.pn_to_mp_objects_in_iterable(ApiVersioning.TYPE.GetAvailableApiVersions(folder if folder else None), constructor.new(_7156.ApiVersion))

    @staticmethod
    def get_available_api_utility_versions(folder: 'str') -> 'Iterable[_7156.ApiVersion]':
        ''' 'GetAvailableApiUtilityVersions' is the original name of this method.

        Args:
            folder (str)

        Returns:
            Iterable[mastapy.scripting.ApiVersion]
        '''

        folder = str(folder)
        return conversion.pn_to_mp_objects_in_iterable(ApiVersioning.TYPE.GetAvailableApiUtilityVersions(folder if folder else None), constructor.new(_7156.ApiVersion))

    @staticmethod
    def get_api_version_for_assembly(api_library_search_folder: 'str', assembly_path: 'str') -> '_7156.ApiVersion':
        ''' 'GetApiVersionForAssembly' is the original name of this method.

        Args:
            api_library_search_folder (str)
            assembly_path (str)

        Returns:
            mastapy.scripting.ApiVersion
        '''

        api_library_search_folder = str(api_library_search_folder)
        assembly_path = str(assembly_path)
        method_result = ApiVersioning.TYPE.GetApiVersionForAssembly(api_library_search_folder if api_library_search_folder else None, assembly_path if assembly_path else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None
