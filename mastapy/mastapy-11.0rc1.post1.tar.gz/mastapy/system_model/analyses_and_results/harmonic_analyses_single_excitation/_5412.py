'''_5412.py

PartToPartShearCouplingHalfHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.part_model.couplings import _2260
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6559
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5368
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_HALF_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'PartToPartShearCouplingHalfHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingHalfHarmonicAnalysisOfSingleExcitation',)


class PartToPartShearCouplingHalfHarmonicAnalysisOfSingleExcitation(_5368.CouplingHalfHarmonicAnalysisOfSingleExcitation):
    '''PartToPartShearCouplingHalfHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_HALF_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingHalfHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2260.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2260.PartToPartShearCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6559.PartToPartShearCouplingHalfLoadCase':
        '''PartToPartShearCouplingHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6559.PartToPartShearCouplingHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
