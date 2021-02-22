'''_4416.py

FEPartCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model import _2126
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4287
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4362
from mastapy._internal.python_net import python_net_import

_FE_PART_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'FEPartCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartCompoundModalAnalysisAtAStiffness',)


class FEPartCompoundModalAnalysisAtAStiffness(_4362.AbstractShaftOrHousingCompoundModalAnalysisAtAStiffness):
    '''FEPartCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _FE_PART_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEPartCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2126.FEPart':
        '''FEPart: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2126.FEPart)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4287.FEPartModalAnalysisAtAStiffness]':
        '''List[FEPartModalAnalysisAtAStiffness]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4287.FEPartModalAnalysisAtAStiffness))
        return value

    @property
    def component_modal_analysis_at_a_stiffness_load_cases(self) -> 'List[_4287.FEPartModalAnalysisAtAStiffness]':
        '''List[FEPartModalAnalysisAtAStiffness]: 'ComponentModalAnalysisAtAStiffnessLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisAtAStiffnessLoadCases, constructor.new(_4287.FEPartModalAnalysisAtAStiffness))
        return value

    @property
    def planetaries(self) -> 'List[FEPartCompoundModalAnalysisAtAStiffness]':
        '''List[FEPartCompoundModalAnalysisAtAStiffness]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(FEPartCompoundModalAnalysisAtAStiffness))
        return value
