'''_5881.py

StraightBevelDiffGearSetCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2217
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5879, _5880, _5792
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5724
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'StraightBevelDiffGearSetCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetCompoundHarmonicAnalysis',)


class StraightBevelDiffGearSetCompoundHarmonicAnalysis(_5792.BevelGearSetCompoundHarmonicAnalysis):
    '''StraightBevelDiffGearSetCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2217.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2217.StraightBevelDiffGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2217.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2217.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def straight_bevel_diff_gears_compound_harmonic_analysis(self) -> 'List[_5879.StraightBevelDiffGearCompoundHarmonicAnalysis]':
        '''List[StraightBevelDiffGearCompoundHarmonicAnalysis]: 'StraightBevelDiffGearsCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsCompoundHarmonicAnalysis, constructor.new(_5879.StraightBevelDiffGearCompoundHarmonicAnalysis))
        return value

    @property
    def straight_bevel_diff_meshes_compound_harmonic_analysis(self) -> 'List[_5880.StraightBevelDiffGearMeshCompoundHarmonicAnalysis]':
        '''List[StraightBevelDiffGearMeshCompoundHarmonicAnalysis]: 'StraightBevelDiffMeshesCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesCompoundHarmonicAnalysis, constructor.new(_5880.StraightBevelDiffGearMeshCompoundHarmonicAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5724.StraightBevelDiffGearSetHarmonicAnalysis]':
        '''List[StraightBevelDiffGearSetHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5724.StraightBevelDiffGearSetHarmonicAnalysis))
        return value

    @property
    def assembly_harmonic_analysis_load_cases(self) -> 'List[_5724.StraightBevelDiffGearSetHarmonicAnalysis]':
        '''List[StraightBevelDiffGearSetHarmonicAnalysis]: 'AssemblyHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyHarmonicAnalysisLoadCases, constructor.new(_5724.StraightBevelDiffGearSetHarmonicAnalysis))
        return value
