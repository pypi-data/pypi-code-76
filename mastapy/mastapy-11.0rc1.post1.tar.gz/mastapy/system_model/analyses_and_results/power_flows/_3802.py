'''_3802.py

StraightBevelDiffGearSetPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _2217
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6592
from mastapy.gears.rating.straight_bevel_diff import _357
from mastapy.system_model.analyses_and_results.power_flows import _3801, _3800, _3710
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'StraightBevelDiffGearSetPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetPowerFlow',)


class StraightBevelDiffGearSetPowerFlow(_3710.BevelGearSetPowerFlow):
    '''StraightBevelDiffGearSetPowerFlow

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2217.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2217.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6592.StraightBevelDiffGearSetLoadCase':
        '''StraightBevelDiffGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6592.StraightBevelDiffGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def rating(self) -> '_357.StraightBevelDiffGearSetRating':
        '''StraightBevelDiffGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_357.StraightBevelDiffGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_357.StraightBevelDiffGearSetRating':
        '''StraightBevelDiffGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_357.StraightBevelDiffGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def gears_power_flow(self) -> 'List[_3801.StraightBevelDiffGearPowerFlow]':
        '''List[StraightBevelDiffGearPowerFlow]: 'GearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsPowerFlow, constructor.new(_3801.StraightBevelDiffGearPowerFlow))
        return value

    @property
    def straight_bevel_diff_gears_power_flow(self) -> 'List[_3801.StraightBevelDiffGearPowerFlow]':
        '''List[StraightBevelDiffGearPowerFlow]: 'StraightBevelDiffGearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsPowerFlow, constructor.new(_3801.StraightBevelDiffGearPowerFlow))
        return value

    @property
    def meshes_power_flow(self) -> 'List[_3800.StraightBevelDiffGearMeshPowerFlow]':
        '''List[StraightBevelDiffGearMeshPowerFlow]: 'MeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesPowerFlow, constructor.new(_3800.StraightBevelDiffGearMeshPowerFlow))
        return value

    @property
    def straight_bevel_diff_meshes_power_flow(self) -> 'List[_3800.StraightBevelDiffGearMeshPowerFlow]':
        '''List[StraightBevelDiffGearMeshPowerFlow]: 'StraightBevelDiffMeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesPowerFlow, constructor.new(_3800.StraightBevelDiffGearMeshPowerFlow))
        return value
