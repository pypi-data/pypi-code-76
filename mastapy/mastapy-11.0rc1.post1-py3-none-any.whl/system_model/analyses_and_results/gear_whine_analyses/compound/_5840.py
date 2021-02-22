'''_5840.py

SynchroniserCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2196
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5449
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5825
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'SynchroniserCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserCompoundGearWhineAnalysis',)


class SynchroniserCompoundGearWhineAnalysis(_5825.SpecialisedAssemblyCompoundGearWhineAnalysis):
    '''SynchroniserCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2196.Synchroniser':
        '''Synchroniser: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2196.Synchroniser)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2196.Synchroniser':
        '''Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2196.Synchroniser)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5449.SynchroniserGearWhineAnalysis]':
        '''List[SynchroniserGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5449.SynchroniserGearWhineAnalysis))
        return value

    @property
    def assembly_gear_whine_analysis_load_cases(self) -> 'List[_5449.SynchroniserGearWhineAnalysis]':
        '''List[SynchroniserGearWhineAnalysis]: 'AssemblyGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyGearWhineAnalysisLoadCases, constructor.new(_5449.SynchroniserGearWhineAnalysis))
        return value
