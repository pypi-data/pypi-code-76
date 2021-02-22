'''_6422.py

SynchroniserHalfCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2275
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6293
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6423
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'SynchroniserHalfCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfCompoundCriticalSpeedAnalysis',)


class SynchroniserHalfCompoundCriticalSpeedAnalysis(_6423.SynchroniserPartCompoundCriticalSpeedAnalysis):
    '''SynchroniserHalfCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_HALF_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserHalfCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2275.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2275.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6293.SynchroniserHalfCriticalSpeedAnalysis]':
        '''List[SynchroniserHalfCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6293.SynchroniserHalfCriticalSpeedAnalysis))
        return value

    @property
    def component_critical_speed_analysis_load_cases(self) -> 'List[_6293.SynchroniserHalfCriticalSpeedAnalysis]':
        '''List[SynchroniserHalfCriticalSpeedAnalysis]: 'ComponentCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentCriticalSpeedAnalysisLoadCases, constructor.new(_6293.SynchroniserHalfCriticalSpeedAnalysis))
        return value
