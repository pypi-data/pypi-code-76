'''_6364.py

FEPartCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2126
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6235
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6310
from mastapy._internal.python_net import python_net_import

_FE_PART_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'FEPartCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartCompoundCriticalSpeedAnalysis',)


class FEPartCompoundCriticalSpeedAnalysis(_6310.AbstractShaftOrHousingCompoundCriticalSpeedAnalysis):
    '''FEPartCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _FE_PART_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEPartCompoundCriticalSpeedAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_6235.FEPartCriticalSpeedAnalysis]':
        '''List[FEPartCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6235.FEPartCriticalSpeedAnalysis))
        return value

    @property
    def component_critical_speed_analysis_load_cases(self) -> 'List[_6235.FEPartCriticalSpeedAnalysis]':
        '''List[FEPartCriticalSpeedAnalysis]: 'ComponentCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentCriticalSpeedAnalysisLoadCases, constructor.new(_6235.FEPartCriticalSpeedAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[FEPartCompoundCriticalSpeedAnalysis]':
        '''List[FEPartCompoundCriticalSpeedAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(FEPartCompoundCriticalSpeedAnalysis))
        return value
