'''_3851.py

ConceptCouplingCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2252
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3720
from mastapy.system_model.analyses_and_results.power_flows.compound import _3862
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'ConceptCouplingCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingCompoundPowerFlow',)


class ConceptCouplingCompoundPowerFlow(_3862.CouplingCompoundPowerFlow):
    '''ConceptCouplingCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2252.ConceptCoupling':
        '''ConceptCoupling: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2252.ConceptCoupling)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2252.ConceptCoupling':
        '''ConceptCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2252.ConceptCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3720.ConceptCouplingPowerFlow]':
        '''List[ConceptCouplingPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3720.ConceptCouplingPowerFlow))
        return value

    @property
    def assembly_power_flow_load_cases(self) -> 'List[_3720.ConceptCouplingPowerFlow]':
        '''List[ConceptCouplingPowerFlow]: 'AssemblyPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyPowerFlowLoadCases, constructor.new(_3720.ConceptCouplingPowerFlow))
        return value
