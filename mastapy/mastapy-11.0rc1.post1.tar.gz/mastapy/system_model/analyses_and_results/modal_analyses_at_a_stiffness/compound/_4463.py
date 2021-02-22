'''_4463.py

SpringDamperConnectionCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _2026
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4333
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4398
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'SpringDamperConnectionCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperConnectionCompoundModalAnalysisAtAStiffness',)


class SpringDamperConnectionCompoundModalAnalysisAtAStiffness(_4398.CouplingConnectionCompoundModalAnalysisAtAStiffness):
    '''SpringDamperConnectionCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperConnectionCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2026.SpringDamperConnection':
        '''SpringDamperConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2026.SpringDamperConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2026.SpringDamperConnection':
        '''SpringDamperConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2026.SpringDamperConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4333.SpringDamperConnectionModalAnalysisAtAStiffness]':
        '''List[SpringDamperConnectionModalAnalysisAtAStiffness]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4333.SpringDamperConnectionModalAnalysisAtAStiffness))
        return value

    @property
    def connection_modal_analysis_at_a_stiffness_load_cases(self) -> 'List[_4333.SpringDamperConnectionModalAnalysisAtAStiffness]':
        '''List[SpringDamperConnectionModalAnalysisAtAStiffness]: 'ConnectionModalAnalysisAtAStiffnessLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysisAtAStiffnessLoadCases, constructor.new(_4333.SpringDamperConnectionModalAnalysisAtAStiffness))
        return value
