'''_2263.py

PartDetailSelection
'''


from typing import Generic, TypeVar

from mastapy._internal import constructor
from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy import _0
from mastapy.system_model.part_model import _2116
from mastapy._internal.python_net import python_net_import

_PART_DETAIL_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'PartDetailSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('PartDetailSelection',)


TPart = TypeVar('TPart', bound='_2116.Part')
TSelectableItem = TypeVar('TSelectableItem')


class PartDetailSelection(_0.APIBase, Generic[TPart, TSelectableItem]):
    '''PartDetailSelection

    This is a mastapy class.

    Generic Types:
        TPart
        TSelectableItem
    '''

    TYPE = _PART_DETAIL_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartDetailSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def selection(self) -> 'list_with_selected_item.ListWithSelectedItem_TSelectableItem':
        '''list_with_selected_item.ListWithSelectedItem_TSelectableItem: 'Selection' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_TSelectableItem)(self.wrapped.Selection) if self.wrapped.Selection else None

    @selection.setter
    def selection(self, value: 'list_with_selected_item.ListWithSelectedItem_TSelectableItem.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_TSelectableItem.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_TSelectableItem.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.Selection = value

    @property
    def selected_item(self) -> 'TSelectableItem':
        '''TSelectableItem: 'SelectedItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(TSelectableItem)(self.wrapped.SelectedItem) if self.wrapped.SelectedItem else None

    @property
    def part(self) -> 'TPart':
        '''TPart: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(TPart)(self.wrapped.Part) if self.wrapped.Part else None
