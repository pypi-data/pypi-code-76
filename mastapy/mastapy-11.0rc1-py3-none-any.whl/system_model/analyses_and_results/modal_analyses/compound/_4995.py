'''_4995.py

ShaftCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.shaft_model import _2154
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4849
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4901
from mastapy._internal.python_net import python_net_import

_SHAFT_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'ShaftCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftCompoundModalAnalysis',)


class ShaftCompoundModalAnalysis(_4901.AbstractShaftCompoundModalAnalysis):
    '''ShaftCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2154.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2154.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4849.ShaftModalAnalysis]':
        '''List[ShaftModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4849.ShaftModalAnalysis))
        return value

    @property
    def component_modal_analysis_load_cases(self) -> 'List[_4849.ShaftModalAnalysis]':
        '''List[ShaftModalAnalysis]: 'ComponentModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisLoadCases, constructor.new(_4849.ShaftModalAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[ShaftCompoundModalAnalysis]':
        '''List[ShaftCompoundModalAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftCompoundModalAnalysis))
        return value
