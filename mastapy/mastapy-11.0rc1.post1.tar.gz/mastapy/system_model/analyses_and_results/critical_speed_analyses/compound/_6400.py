'''_6400.py

RollingRingCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2267
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6272
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6347
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'RollingRingCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingCompoundCriticalSpeedAnalysis',)


class RollingRingCompoundCriticalSpeedAnalysis(_6347.CouplingHalfCompoundCriticalSpeedAnalysis):
    '''RollingRingCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingCompoundCriticalSpeedAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_6272.RollingRingCriticalSpeedAnalysis]':
        '''List[RollingRingCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6272.RollingRingCriticalSpeedAnalysis))
        return value

    @property
    def component_critical_speed_analysis_load_cases(self) -> 'List[_6272.RollingRingCriticalSpeedAnalysis]':
        '''List[RollingRingCriticalSpeedAnalysis]: 'ComponentCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentCriticalSpeedAnalysisLoadCases, constructor.new(_6272.RollingRingCriticalSpeedAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[RollingRingCompoundCriticalSpeedAnalysis]':
        '''List[RollingRingCompoundCriticalSpeedAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingCompoundCriticalSpeedAnalysis))
        return value
