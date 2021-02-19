'''_3522.py

WormGearSetCompoundPowerFlow
'''


from typing import List

from mastapy.gears.rating.worm import _174
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import _2150
from mastapy.system_model.analyses_and_results.power_flows.compound import _3520, _3521, _3458
from mastapy.system_model.analyses_and_results.power_flows import _3401
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'WormGearSetCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetCompoundPowerFlow',)


class WormGearSetCompoundPowerFlow(_3458.GearSetCompoundPowerFlow):
    '''WormGearSetCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_set_duty_cycle_rating(self) -> '_174.WormGearSetDutyCycleRating':
        '''WormGearSetDutyCycleRating: 'GearSetDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_174.WormGearSetDutyCycleRating)(self.wrapped.GearSetDutyCycleRating) if self.wrapped.GearSetDutyCycleRating else None

    @property
    def worm_gear_set_duty_cycle_rating(self) -> '_174.WormGearSetDutyCycleRating':
        '''WormGearSetDutyCycleRating: 'WormGearSetDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_174.WormGearSetDutyCycleRating)(self.wrapped.WormGearSetDutyCycleRating) if self.wrapped.WormGearSetDutyCycleRating else None

    @property
    def component_design(self) -> '_2150.WormGearSet':
        '''WormGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2150.WormGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2150.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2150.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def worm_gears_compound_power_flow(self) -> 'List[_3520.WormGearCompoundPowerFlow]':
        '''List[WormGearCompoundPowerFlow]: 'WormGearsCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsCompoundPowerFlow, constructor.new(_3520.WormGearCompoundPowerFlow))
        return value

    @property
    def worm_meshes_compound_power_flow(self) -> 'List[_3521.WormGearMeshCompoundPowerFlow]':
        '''List[WormGearMeshCompoundPowerFlow]: 'WormMeshesCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesCompoundPowerFlow, constructor.new(_3521.WormGearMeshCompoundPowerFlow))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3401.WormGearSetPowerFlow]':
        '''List[WormGearSetPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3401.WormGearSetPowerFlow))
        return value

    @property
    def assembly_power_flow_load_cases(self) -> 'List[_3401.WormGearSetPowerFlow]':
        '''List[WormGearSetPowerFlow]: 'AssemblyPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyPowerFlowLoadCases, constructor.new(_3401.WormGearSetPowerFlow))
        return value
