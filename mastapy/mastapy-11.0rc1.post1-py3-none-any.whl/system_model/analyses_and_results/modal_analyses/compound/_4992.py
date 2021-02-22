'''_4992.py

RollingRingCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2267
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4846
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4939
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'RollingRingCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingCompoundModalAnalysis',)


class RollingRingCompoundModalAnalysis(_4939.CouplingHalfCompoundModalAnalysis):
    '''RollingRingCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingCompoundModalAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_4846.RollingRingModalAnalysis]':
        '''List[RollingRingModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4846.RollingRingModalAnalysis))
        return value

    @property
    def component_modal_analysis_load_cases(self) -> 'List[_4846.RollingRingModalAnalysis]':
        '''List[RollingRingModalAnalysis]: 'ComponentModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisLoadCases, constructor.new(_4846.RollingRingModalAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[RollingRingCompoundModalAnalysis]':
        '''List[RollingRingCompoundModalAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingCompoundModalAnalysis))
        return value
