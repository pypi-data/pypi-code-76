'''_5439.py

StraightBevelGearHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.part_model.gears import _2218
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6593
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5346
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'StraightBevelGearHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearHarmonicAnalysisOfSingleExcitation',)


class StraightBevelGearHarmonicAnalysisOfSingleExcitation(_5346.BevelGearHarmonicAnalysisOfSingleExcitation):
    '''StraightBevelGearHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2218.StraightBevelGear':
        '''StraightBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2218.StraightBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6593.StraightBevelGearLoadCase':
        '''StraightBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6593.StraightBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
