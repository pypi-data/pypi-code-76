'''_5445.py

SynchroniserHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.part_model.couplings import _2273
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6599
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5429
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'SynchroniserHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHarmonicAnalysisOfSingleExcitation',)


class SynchroniserHarmonicAnalysisOfSingleExcitation(_5429.SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation):
    '''SynchroniserHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2273.Synchroniser':
        '''Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2273.Synchroniser)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6599.SynchroniserLoadCase':
        '''SynchroniserLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6599.SynchroniserLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
