'''_5373.py

CycloidalAssemblyHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.part_model.cycloidal import _2239
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6488
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5429
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_ASSEMBLY_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'CycloidalAssemblyHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalAssemblyHarmonicAnalysisOfSingleExcitation',)


class CycloidalAssemblyHarmonicAnalysisOfSingleExcitation(_5429.SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation):
    '''CycloidalAssemblyHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_ASSEMBLY_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalAssemblyHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2239.CycloidalAssembly':
        '''CycloidalAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2239.CycloidalAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6488.CycloidalAssemblyLoadCase':
        '''CycloidalAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6488.CycloidalAssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
