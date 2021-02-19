'''_3501.py

SpringDamperHalfCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2195
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3378
from mastapy.system_model.analyses_and_results.power_flows.compound import _3442
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_HALF_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'SpringDamperHalfCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperHalfCompoundPowerFlow',)


class SpringDamperHalfCompoundPowerFlow(_3442.CouplingHalfCompoundPowerFlow):
    '''SpringDamperHalfCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_HALF_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperHalfCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2195.SpringDamperHalf':
        '''SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2195.SpringDamperHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3378.SpringDamperHalfPowerFlow]':
        '''List[SpringDamperHalfPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3378.SpringDamperHalfPowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_3378.SpringDamperHalfPowerFlow]':
        '''List[SpringDamperHalfPowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_3378.SpringDamperHalfPowerFlow))
        return value
