'''_3505.py

StraightBevelGearCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _2145
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3384
from mastapy.system_model.analyses_and_results.power_flows.compound import _3419
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'StraightBevelGearCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearCompoundPowerFlow',)


class StraightBevelGearCompoundPowerFlow(_3419.BevelGearCompoundPowerFlow):
    '''StraightBevelGearCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2145.StraightBevelGear':
        '''StraightBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2145.StraightBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3384.StraightBevelGearPowerFlow]':
        '''List[StraightBevelGearPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3384.StraightBevelGearPowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_3384.StraightBevelGearPowerFlow]':
        '''List[StraightBevelGearPowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_3384.StraightBevelGearPowerFlow))
        return value
