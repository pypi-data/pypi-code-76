'''_3870.py

CycloidalDiscCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2240
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3738
from mastapy.system_model.analyses_and_results.power_flows.compound import _3826
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'CycloidalDiscCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscCompoundPowerFlow',)


class CycloidalDiscCompoundPowerFlow(_3826.AbstractShaftCompoundPowerFlow):
    '''CycloidalDiscCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2240.CycloidalDisc':
        '''CycloidalDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2240.CycloidalDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3738.CycloidalDiscPowerFlow]':
        '''List[CycloidalDiscPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3738.CycloidalDiscPowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_3738.CycloidalDiscPowerFlow]':
        '''List[CycloidalDiscPowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_3738.CycloidalDiscPowerFlow))
        return value
