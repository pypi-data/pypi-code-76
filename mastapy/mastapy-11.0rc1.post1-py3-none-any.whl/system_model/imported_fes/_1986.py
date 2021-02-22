'''_1986.py

FEEntityGroupWithSelection
'''


from typing import Callable, Generic, TypeVar

from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_FE_ENTITY_GROUP_WITH_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'FEEntityGroupWithSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('FEEntityGroupWithSelection',)


TGroup = TypeVar('TGroup', bound='')
TGroupContents = TypeVar('TGroupContents')


class FEEntityGroupWithSelection(_0.APIBase, Generic[TGroup, TGroupContents]):
    '''FEEntityGroupWithSelection

    This is a mastapy class.

    Generic Types:
        TGroup
        TGroupContents
    '''

    TYPE = _FE_ENTITY_GROUP_WITH_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEEntityGroupWithSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def add_selection_to_group(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'AddSelectionToGroup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddSelectionToGroup

    @property
    def select_items(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SelectItems' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectItems

    @property
    def delete_group(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'DeleteGroup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DeleteGroup

    @property
    def group(self) -> 'TGroup':
        '''TGroup: 'Group' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(TGroup)(self.wrapped.Group) if self.wrapped.Group else None
