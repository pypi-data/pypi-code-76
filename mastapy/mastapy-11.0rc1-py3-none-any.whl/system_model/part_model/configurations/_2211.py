'''_2211.py

PartDetailConfiguration
'''


from typing import (
    Callable, List, Generic, TypeVar
)

from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy.system_model.part_model import _2068
from mastapy._internal.python_net import python_net_import

_PART_DETAIL_CONFIGURATION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'PartDetailConfiguration')


__docformat__ = 'restructuredtext en'
__all__ = ('PartDetailConfiguration',)


TPartDetailSelection = TypeVar('TPartDetailSelection', bound='')
TPart = TypeVar('TPart', bound='_2068.Part')
TSelectableItem = TypeVar('TSelectableItem')


class PartDetailConfiguration(_0.APIBase, Generic[TPartDetailSelection, TPart, TSelectableItem]):
    '''PartDetailConfiguration

    This is a mastapy class.

    Generic Types:
        TPartDetailSelection
        TPart
        TSelectableItem
    '''

    TYPE = _PART_DETAIL_CONFIGURATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartDetailConfiguration.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def delete_configuration(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'DeleteConfiguration' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DeleteConfiguration

    @property
    def select_configuration(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SelectConfiguration' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectConfiguration

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None

    @property
    def selections(self) -> 'List[TPartDetailSelection]':
        '''List[TPartDetailSelection]: 'Selections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Selections, constructor.new(TPartDetailSelection))
        return value
