'''_3338.py

HypoidGearSetPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _2133
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6205
from mastapy.gears.rating.hypoid import _239
from mastapy.system_model.analyses_and_results.power_flows import _3337, _3336, _3284
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'HypoidGearSetPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetPowerFlow',)


class HypoidGearSetPowerFlow(_3284.AGMAGleasonConicalGearSetPowerFlow):
    '''HypoidGearSetPowerFlow

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2133.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2133.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6205.HypoidGearSetLoadCase':
        '''HypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6205.HypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def rating(self) -> '_239.HypoidGearSetRating':
        '''HypoidGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_239.HypoidGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_239.HypoidGearSetRating':
        '''HypoidGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_239.HypoidGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def gears_power_flow(self) -> 'List[_3337.HypoidGearPowerFlow]':
        '''List[HypoidGearPowerFlow]: 'GearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsPowerFlow, constructor.new(_3337.HypoidGearPowerFlow))
        return value

    @property
    def hypoid_gears_power_flow(self) -> 'List[_3337.HypoidGearPowerFlow]':
        '''List[HypoidGearPowerFlow]: 'HypoidGearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsPowerFlow, constructor.new(_3337.HypoidGearPowerFlow))
        return value

    @property
    def meshes_power_flow(self) -> 'List[_3336.HypoidGearMeshPowerFlow]':
        '''List[HypoidGearMeshPowerFlow]: 'MeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesPowerFlow, constructor.new(_3336.HypoidGearMeshPowerFlow))
        return value

    @property
    def hypoid_meshes_power_flow(self) -> 'List[_3336.HypoidGearMeshPowerFlow]':
        '''List[HypoidGearMeshPowerFlow]: 'HypoidMeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesPowerFlow, constructor.new(_3336.HypoidGearMeshPowerFlow))
        return value
