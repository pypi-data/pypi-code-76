'''_1975.py

ContactPairWithSelection
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting import _1498
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CONTACT_PAIR_WITH_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ContactPairWithSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('ContactPairWithSelection',)


class ContactPairWithSelection(_0.APIBase):
    '''ContactPairWithSelection

    This is a mastapy class.
    '''

    TYPE = _CONTACT_PAIR_WITH_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ContactPairWithSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def select_reference_surface(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SelectReferenceSurface' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectReferenceSurface

    @property
    def select_constrained_surface(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SelectConstrainedSurface' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectConstrainedSurface

    @property
    def select_contacting_reference_surface(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SelectContactingReferenceSurface' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectContactingReferenceSurface

    @property
    def select_contacting_constrained_surface(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SelectContactingConstrainedSurface' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectContactingConstrainedSurface

    @property
    def contact_pair(self) -> '_1498.ContactPairReporting':
        '''ContactPairReporting: 'ContactPair' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1498.ContactPairReporting)(self.wrapped.ContactPair) if self.wrapped.ContactPair else None
