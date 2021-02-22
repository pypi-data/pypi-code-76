'''_2499.py

PointLoadCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2071
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2361
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2534
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'PointLoadCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadCompoundSystemDeflection',)


class PointLoadCompoundSystemDeflection(_2534.VirtualComponentCompoundSystemDeflection):
    '''PointLoadCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2071.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2071.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2361.PointLoadSystemDeflection]':
        '''List[PointLoadSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2361.PointLoadSystemDeflection))
        return value

    @property
    def component_system_deflection_load_cases(self) -> 'List[_2361.PointLoadSystemDeflection]':
        '''List[PointLoadSystemDeflection]: 'ComponentSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionLoadCases, constructor.new(_2361.PointLoadSystemDeflection))
        return value
