'''_5558.py

SpecialisedAssemblyCompoundHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import _5460
from mastapy._internal.python_net import python_net_import

_SPECIALISED_ASSEMBLY_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound', 'SpecialisedAssemblyCompoundHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('SpecialisedAssemblyCompoundHarmonicAnalysisOfSingleExcitation',)


class SpecialisedAssemblyCompoundHarmonicAnalysisOfSingleExcitation(_5460.AbstractAssemblyCompoundHarmonicAnalysisOfSingleExcitation):
    '''SpecialisedAssemblyCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _SPECIALISED_ASSEMBLY_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpecialisedAssemblyCompoundHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
