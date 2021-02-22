'''_4646.py

ConceptCouplingHalfCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2253
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4516
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4657
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_HALF_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'ConceptCouplingHalfCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingHalfCompoundModalAnalysisAtASpeed',)


class ConceptCouplingHalfCompoundModalAnalysisAtASpeed(_4657.CouplingHalfCompoundModalAnalysisAtASpeed):
    '''ConceptCouplingHalfCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_HALF_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingHalfCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2253.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2253.ConceptCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4516.ConceptCouplingHalfModalAnalysisAtASpeed]':
        '''List[ConceptCouplingHalfModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4516.ConceptCouplingHalfModalAnalysisAtASpeed))
        return value

    @property
    def component_modal_analysis_at_a_speed_load_cases(self) -> 'List[_4516.ConceptCouplingHalfModalAnalysisAtASpeed]':
        '''List[ConceptCouplingHalfModalAnalysisAtASpeed]: 'ComponentModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisAtASpeedLoadCases, constructor.new(_4516.ConceptCouplingHalfModalAnalysisAtASpeed))
        return value
