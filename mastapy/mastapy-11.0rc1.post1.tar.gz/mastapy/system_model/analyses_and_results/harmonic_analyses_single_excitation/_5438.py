'''_5438.py

StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2217
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6592
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5436, _5437, _5348
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation',)


class StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation(_5348.BevelGearSetHarmonicAnalysisOfSingleExcitation):
    '''StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2217.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2217.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6592.StraightBevelDiffGearSetLoadCase':
        '''StraightBevelDiffGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6592.StraightBevelDiffGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def straight_bevel_diff_gears_harmonic_analysis_of_single_excitation(self) -> 'List[_5436.StraightBevelDiffGearHarmonicAnalysisOfSingleExcitation]':
        '''List[StraightBevelDiffGearHarmonicAnalysisOfSingleExcitation]: 'StraightBevelDiffGearsHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsHarmonicAnalysisOfSingleExcitation, constructor.new(_5436.StraightBevelDiffGearHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def straight_bevel_diff_meshes_harmonic_analysis_of_single_excitation(self) -> 'List[_5437.StraightBevelDiffGearMeshHarmonicAnalysisOfSingleExcitation]':
        '''List[StraightBevelDiffGearMeshHarmonicAnalysisOfSingleExcitation]: 'StraightBevelDiffMeshesHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesHarmonicAnalysisOfSingleExcitation, constructor.new(_5437.StraightBevelDiffGearMeshHarmonicAnalysisOfSingleExcitation))
        return value
