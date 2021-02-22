'''_3889.py

HypoidGearSetCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _2206
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows.compound import _3887, _3888, _3831
from mastapy.system_model.analyses_and_results.power_flows import _3757
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'HypoidGearSetCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetCompoundPowerFlow',)


class HypoidGearSetCompoundPowerFlow(_3831.AGMAGleasonConicalGearSetCompoundPowerFlow):
    '''HypoidGearSetCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2206.HypoidGearSet':
        '''HypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2206.HypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2206.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2206.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def hypoid_gears_compound_power_flow(self) -> 'List[_3887.HypoidGearCompoundPowerFlow]':
        '''List[HypoidGearCompoundPowerFlow]: 'HypoidGearsCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsCompoundPowerFlow, constructor.new(_3887.HypoidGearCompoundPowerFlow))
        return value

    @property
    def hypoid_meshes_compound_power_flow(self) -> 'List[_3888.HypoidGearMeshCompoundPowerFlow]':
        '''List[HypoidGearMeshCompoundPowerFlow]: 'HypoidMeshesCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesCompoundPowerFlow, constructor.new(_3888.HypoidGearMeshCompoundPowerFlow))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3757.HypoidGearSetPowerFlow]':
        '''List[HypoidGearSetPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3757.HypoidGearSetPowerFlow))
        return value

    @property
    def assembly_power_flow_load_cases(self) -> 'List[_3757.HypoidGearSetPowerFlow]':
        '''List[HypoidGearSetPowerFlow]: 'AssemblyPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyPowerFlowLoadCases, constructor.new(_3757.HypoidGearSetPowerFlow))
        return value
