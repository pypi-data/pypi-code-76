'''_1960.py

CoordinateSystemWithSelection
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting import _1498
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_COORDINATE_SYSTEM_WITH_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'CoordinateSystemWithSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('CoordinateSystemWithSelection',)


class CoordinateSystemWithSelection(_0.APIBase):
    '''CoordinateSystemWithSelection

    This is a mastapy class.
    '''

    TYPE = _COORDINATE_SYSTEM_WITH_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CoordinateSystemWithSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def select_nodes_using_this_for_material_orientation(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SelectNodesUsingThisForMaterialOrientation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectNodesUsingThisForMaterialOrientation

    @property
    def coordinate_system(self) -> '_1498.CoordinateSystemReporting':
        '''CoordinateSystemReporting: 'CoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1498.CoordinateSystemReporting)(self.wrapped.CoordinateSystem) if self.wrapped.CoordinateSystem else None
