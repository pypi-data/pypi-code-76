'''_6397.py

RingPinsCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2241
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6268
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6385
from mastapy._internal.python_net import python_net_import

_RING_PINS_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'RingPinsCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsCompoundCriticalSpeedAnalysis',)


class RingPinsCompoundCriticalSpeedAnalysis(_6385.MountableComponentCompoundCriticalSpeedAnalysis):
    '''RingPinsCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2241.RingPins':
        '''RingPins: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2241.RingPins)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6268.RingPinsCriticalSpeedAnalysis]':
        '''List[RingPinsCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6268.RingPinsCriticalSpeedAnalysis))
        return value

    @property
    def component_critical_speed_analysis_load_cases(self) -> 'List[_6268.RingPinsCriticalSpeedAnalysis]':
        '''List[RingPinsCriticalSpeedAnalysis]: 'ComponentCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentCriticalSpeedAnalysisLoadCases, constructor.new(_6268.RingPinsCriticalSpeedAnalysis))
        return value
