'''_3946.py

UnbalancedMassCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model import _2150
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3817
from mastapy.system_model.analyses_and_results.power_flows.compound import _3947
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'UnbalancedMassCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassCompoundPowerFlow',)


class UnbalancedMassCompoundPowerFlow(_3947.VirtualComponentCompoundPowerFlow):
    '''UnbalancedMassCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2150.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2150.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3817.UnbalancedMassPowerFlow]':
        '''List[UnbalancedMassPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3817.UnbalancedMassPowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_3817.UnbalancedMassPowerFlow]':
        '''List[UnbalancedMassPowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_3817.UnbalancedMassPowerFlow))
        return value
