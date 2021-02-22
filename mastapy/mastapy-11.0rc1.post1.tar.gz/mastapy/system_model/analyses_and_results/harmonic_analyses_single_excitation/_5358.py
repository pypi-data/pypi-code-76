'''_5358.py

ConceptCouplingHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.part_model.couplings import _2252
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6471
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5369
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'ConceptCouplingHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingHarmonicAnalysisOfSingleExcitation',)


class ConceptCouplingHarmonicAnalysisOfSingleExcitation(_5369.CouplingHarmonicAnalysisOfSingleExcitation):
    '''ConceptCouplingHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2252.ConceptCoupling':
        '''ConceptCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2252.ConceptCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6471.ConceptCouplingLoadCase':
        '''ConceptCouplingLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6471.ConceptCouplingLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
