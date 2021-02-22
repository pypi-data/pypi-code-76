'''_4956.py

FEPartCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2126
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4804
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4902
from mastapy._internal.python_net import python_net_import

_FE_PART_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'FEPartCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartCompoundModalAnalysis',)


class FEPartCompoundModalAnalysis(_4902.AbstractShaftOrHousingCompoundModalAnalysis):
    '''FEPartCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _FE_PART_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEPartCompoundModalAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_4804.FEPartModalAnalysis]':
        '''List[FEPartModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4804.FEPartModalAnalysis))
        return value

    @property
    def component_modal_analysis_load_cases(self) -> 'List[_4804.FEPartModalAnalysis]':
        '''List[FEPartModalAnalysis]: 'ComponentModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisLoadCases, constructor.new(_4804.FEPartModalAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[FEPartCompoundModalAnalysis]':
        '''List[FEPartCompoundModalAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(FEPartCompoundModalAnalysis))
        return value
