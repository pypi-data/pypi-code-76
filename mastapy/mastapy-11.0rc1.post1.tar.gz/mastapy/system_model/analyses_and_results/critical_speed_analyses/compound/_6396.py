'''_6396.py

PulleyCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2261, _2258
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6267
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6347
from mastapy._internal.python_net import python_net_import

_PULLEY_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'PulleyCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleyCompoundCriticalSpeedAnalysis',)


class PulleyCompoundCriticalSpeedAnalysis(_6347.CouplingHalfCompoundCriticalSpeedAnalysis):
    '''PulleyCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _PULLEY_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleyCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2261.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2261.Pulley.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Pulley. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6267.PulleyCriticalSpeedAnalysis]':
        '''List[PulleyCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6267.PulleyCriticalSpeedAnalysis))
        return value

    @property
    def component_critical_speed_analysis_load_cases(self) -> 'List[_6267.PulleyCriticalSpeedAnalysis]':
        '''List[PulleyCriticalSpeedAnalysis]: 'ComponentCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentCriticalSpeedAnalysisLoadCases, constructor.new(_6267.PulleyCriticalSpeedAnalysis))
        return value
