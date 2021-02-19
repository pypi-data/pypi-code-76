'''_2474.py

HypoidGearCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2132
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2335
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2420
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'HypoidGearCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearCompoundSystemDeflection',)


class HypoidGearCompoundSystemDeflection(_2420.AGMAGleasonConicalGearCompoundSystemDeflection):
    '''HypoidGearCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2132.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2132.HypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2335.HypoidGearSystemDeflection]':
        '''List[HypoidGearSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2335.HypoidGearSystemDeflection))
        return value

    @property
    def component_system_deflection_load_cases(self) -> 'List[_2335.HypoidGearSystemDeflection]':
        '''List[HypoidGearSystemDeflection]: 'ComponentSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionLoadCases, constructor.new(_2335.HypoidGearSystemDeflection))
        return value
