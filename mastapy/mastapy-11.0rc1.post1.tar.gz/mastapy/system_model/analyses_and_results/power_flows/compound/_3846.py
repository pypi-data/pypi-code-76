'''_3846.py

ClutchCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2249
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3715
from mastapy.system_model.analyses_and_results.power_flows.compound import _3862
from mastapy._internal.python_net import python_net_import

_CLUTCH_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'ClutchCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchCompoundPowerFlow',)


class ClutchCompoundPowerFlow(_3862.CouplingCompoundPowerFlow):
    '''ClutchCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2249.Clutch':
        '''Clutch: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2249.Clutch)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2249.Clutch':
        '''Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2249.Clutch)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3715.ClutchPowerFlow]':
        '''List[ClutchPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3715.ClutchPowerFlow))
        return value

    @property
    def assembly_power_flow_load_cases(self) -> 'List[_3715.ClutchPowerFlow]':
        '''List[ClutchPowerFlow]: 'AssemblyPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyPowerFlowLoadCases, constructor.new(_3715.ClutchPowerFlow))
        return value
