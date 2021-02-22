'''_3868.py

CycloidalAssemblyCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2239
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3735
from mastapy.system_model.analyses_and_results.power_flows.compound import _3923
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_ASSEMBLY_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'CycloidalAssemblyCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalAssemblyCompoundPowerFlow',)


class CycloidalAssemblyCompoundPowerFlow(_3923.SpecialisedAssemblyCompoundPowerFlow):
    '''CycloidalAssemblyCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_ASSEMBLY_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalAssemblyCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2239.CycloidalAssembly':
        '''CycloidalAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2239.CycloidalAssembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2239.CycloidalAssembly':
        '''CycloidalAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2239.CycloidalAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3735.CycloidalAssemblyPowerFlow]':
        '''List[CycloidalAssemblyPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3735.CycloidalAssemblyPowerFlow))
        return value

    @property
    def assembly_power_flow_load_cases(self) -> 'List[_3735.CycloidalAssemblyPowerFlow]':
        '''List[CycloidalAssemblyPowerFlow]: 'AssemblyPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyPowerFlowLoadCases, constructor.new(_3735.CycloidalAssemblyPowerFlow))
        return value
