'''_6429.py

UnbalancedMassCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2150
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6300
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6430
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'UnbalancedMassCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassCompoundCriticalSpeedAnalysis',)


class UnbalancedMassCompoundCriticalSpeedAnalysis(_6430.VirtualComponentCompoundCriticalSpeedAnalysis):
    '''UnbalancedMassCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2150.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2150.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6300.UnbalancedMassCriticalSpeedAnalysis]':
        '''List[UnbalancedMassCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6300.UnbalancedMassCriticalSpeedAnalysis))
        return value

    @property
    def component_critical_speed_analysis_load_cases(self) -> 'List[_6300.UnbalancedMassCriticalSpeedAnalysis]':
        '''List[UnbalancedMassCriticalSpeedAnalysis]: 'ComponentCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentCriticalSpeedAnalysisLoadCases, constructor.new(_6300.UnbalancedMassCriticalSpeedAnalysis))
        return value
