'''_1366.py

DeletableCollectionMember
'''


from typing import Callable, Generic, TypeVar

from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_DELETABLE_COLLECTION_MEMBER = python_net_import('SMT.MastaAPI.Utility.Property', 'DeletableCollectionMember')


__docformat__ = 'restructuredtext en'
__all__ = ('DeletableCollectionMember',)


T = TypeVar('T')


class DeletableCollectionMember(_0.APIBase, Generic[T]):
    '''DeletableCollectionMember

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _DELETABLE_COLLECTION_MEMBER

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DeletableCollectionMember.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def delete(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'Delete' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Delete

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def item(self) -> 'T':
        '''T: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(T)(self.wrapped.Item) if self.wrapped.Item else None
