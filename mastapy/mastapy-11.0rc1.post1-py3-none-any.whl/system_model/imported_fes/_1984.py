'''_1984.py

ElementPropertiesWithSelection
'''


from typing import Callable, Generic, TypeVar

from mastapy._internal import constructor
from mastapy import _0
from mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting import _1503
from mastapy._internal.python_net import python_net_import

_ELEMENT_PROPERTIES_WITH_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ElementPropertiesWithSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('ElementPropertiesWithSelection',)


T = TypeVar('T', bound='_1503.ElementPropertiesBase')


class ElementPropertiesWithSelection(_0.APIBase, Generic[T]):
    '''ElementPropertiesWithSelection

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _ELEMENT_PROPERTIES_WITH_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ElementPropertiesWithSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def select_nodes(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SelectNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectNodes

    @property
    def element_properties(self) -> 'T':
        '''T: 'ElementProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(T)(self.wrapped.ElementProperties) if self.wrapped.ElementProperties else None
