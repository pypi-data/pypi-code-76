'''_4452.py

RollingRingCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2267
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4324
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4399
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'RollingRingCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingCompoundModalAnalysisAtAStiffness',)


class RollingRingCompoundModalAnalysisAtAStiffness(_4399.CouplingHalfCompoundModalAnalysisAtAStiffness):
    '''RollingRingCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2267.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2267.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4324.RollingRingModalAnalysisAtAStiffness]':
        '''List[RollingRingModalAnalysisAtAStiffness]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4324.RollingRingModalAnalysisAtAStiffness))
        return value

    @property
    def component_modal_analysis_at_a_stiffness_load_cases(self) -> 'List[_4324.RollingRingModalAnalysisAtAStiffness]':
        '''List[RollingRingModalAnalysisAtAStiffness]: 'ComponentModalAnalysisAtAStiffnessLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisAtAStiffnessLoadCases, constructor.new(_4324.RollingRingModalAnalysisAtAStiffness))
        return value

    @property
    def planetaries(self) -> 'List[RollingRingCompoundModalAnalysisAtAStiffness]':
        '''List[RollingRingCompoundModalAnalysisAtAStiffness]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingCompoundModalAnalysisAtAStiffness))
        return value
