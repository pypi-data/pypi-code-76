'''_5544.py

PlanetaryGearSetCompoundHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import _5509
from mastapy._internal.python_net import python_net_import

_PLANETARY_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound', 'PlanetaryGearSetCompoundHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryGearSetCompoundHarmonicAnalysisOfSingleExcitation',)


class PlanetaryGearSetCompoundHarmonicAnalysisOfSingleExcitation(_5509.CylindricalGearSetCompoundHarmonicAnalysisOfSingleExcitation):
    '''PlanetaryGearSetCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryGearSetCompoundHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
