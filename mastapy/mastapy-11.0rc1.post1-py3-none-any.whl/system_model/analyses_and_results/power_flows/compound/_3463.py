'''_3463.py

ImportedFEComponentCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model import _2058
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3339
from mastapy.system_model.analyses_and_results.power_flows.compound import _3406
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_COMPONENT_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'ImportedFEComponentCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEComponentCompoundPowerFlow',)


class ImportedFEComponentCompoundPowerFlow(_3406.AbstractShaftOrHousingCompoundPowerFlow):
    '''ImportedFEComponentCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_COMPONENT_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEComponentCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2058.ImportedFEComponent':
        '''ImportedFEComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2058.ImportedFEComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3339.ImportedFEComponentPowerFlow]':
        '''List[ImportedFEComponentPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3339.ImportedFEComponentPowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_3339.ImportedFEComponentPowerFlow]':
        '''List[ImportedFEComponentPowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_3339.ImportedFEComponentPowerFlow))
        return value
