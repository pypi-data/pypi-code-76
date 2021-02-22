'''_6327.py

BoltCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2116
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6196
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6333
from mastapy._internal.python_net import python_net_import

_BOLT_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'BoltCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltCompoundCriticalSpeedAnalysis',)


class BoltCompoundCriticalSpeedAnalysis(_6333.ComponentCompoundCriticalSpeedAnalysis):
    '''BoltCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _BOLT_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2116.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2116.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6196.BoltCriticalSpeedAnalysis]':
        '''List[BoltCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6196.BoltCriticalSpeedAnalysis))
        return value

    @property
    def component_critical_speed_analysis_load_cases(self) -> 'List[_6196.BoltCriticalSpeedAnalysis]':
        '''List[BoltCriticalSpeedAnalysis]: 'ComponentCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentCriticalSpeedAnalysisLoadCases, constructor.new(_6196.BoltCriticalSpeedAnalysis))
        return value
