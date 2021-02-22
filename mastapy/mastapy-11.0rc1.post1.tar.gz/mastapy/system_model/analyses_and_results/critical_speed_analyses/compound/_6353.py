'''_6353.py

CycloidalDiscCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2240
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6224
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6309
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'CycloidalDiscCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscCompoundCriticalSpeedAnalysis',)


class CycloidalDiscCompoundCriticalSpeedAnalysis(_6309.AbstractShaftCompoundCriticalSpeedAnalysis):
    '''CycloidalDiscCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2240.CycloidalDisc':
        '''CycloidalDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2240.CycloidalDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6224.CycloidalDiscCriticalSpeedAnalysis]':
        '''List[CycloidalDiscCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6224.CycloidalDiscCriticalSpeedAnalysis))
        return value

    @property
    def component_critical_speed_analysis_load_cases(self) -> 'List[_6224.CycloidalDiscCriticalSpeedAnalysis]':
        '''List[CycloidalDiscCriticalSpeedAnalysis]: 'ComponentCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentCriticalSpeedAnalysisLoadCases, constructor.new(_6224.CycloidalDiscCriticalSpeedAnalysis))
        return value
