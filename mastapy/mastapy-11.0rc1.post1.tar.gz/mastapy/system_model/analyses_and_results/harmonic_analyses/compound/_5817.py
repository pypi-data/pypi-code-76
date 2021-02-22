'''_5817.py

CycloidalAssemblyCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2239
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5634
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5872
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_ASSEMBLY_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'CycloidalAssemblyCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalAssemblyCompoundHarmonicAnalysis',)


class CycloidalAssemblyCompoundHarmonicAnalysis(_5872.SpecialisedAssemblyCompoundHarmonicAnalysis):
    '''CycloidalAssemblyCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_ASSEMBLY_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalAssemblyCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2239.CycloidalAssembly':
        '''CycloidalAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2239.CycloidalAssembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2239.CycloidalAssembly':
        '''CycloidalAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2239.CycloidalAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5634.CycloidalAssemblyHarmonicAnalysis]':
        '''List[CycloidalAssemblyHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5634.CycloidalAssemblyHarmonicAnalysis))
        return value

    @property
    def assembly_harmonic_analysis_load_cases(self) -> 'List[_5634.CycloidalAssemblyHarmonicAnalysis]':
        '''List[CycloidalAssemblyHarmonicAnalysis]: 'AssemblyHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyHarmonicAnalysisLoadCases, constructor.new(_5634.CycloidalAssemblyHarmonicAnalysis))
        return value
