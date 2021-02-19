'''_1988.py

FEStiffnessGeometry
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_FE_STIFFNESS_GEOMETRY = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'FEStiffnessGeometry')


__docformat__ = 'restructuredtext en'
__all__ = ('FEStiffnessGeometry',)


class FEStiffnessGeometry(_0.APIBase):
    '''FEStiffnessGeometry

    This is a mastapy class.
    '''

    TYPE = _FE_STIFFNESS_GEOMETRY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEStiffnessGeometry.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None

    @property
    def delete_geometry(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'DeleteGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DeleteGeometry

    @property
    def reduce_file_size(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ReduceFileSize' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReduceFileSize
