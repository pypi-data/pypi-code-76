'''_6421.py

SynchroniserCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2273
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6292
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6406
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'SynchroniserCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserCompoundCriticalSpeedAnalysis',)


class SynchroniserCompoundCriticalSpeedAnalysis(_6406.SpecialisedAssemblyCompoundCriticalSpeedAnalysis):
    '''SynchroniserCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2273.Synchroniser':
        '''Synchroniser: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2273.Synchroniser)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2273.Synchroniser':
        '''Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2273.Synchroniser)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6292.SynchroniserCriticalSpeedAnalysis]':
        '''List[SynchroniserCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6292.SynchroniserCriticalSpeedAnalysis))
        return value

    @property
    def assembly_critical_speed_analysis_load_cases(self) -> 'List[_6292.SynchroniserCriticalSpeedAnalysis]':
        '''List[SynchroniserCriticalSpeedAnalysis]: 'AssemblyCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyCriticalSpeedAnalysisLoadCases, constructor.new(_6292.SynchroniserCriticalSpeedAnalysis))
        return value
