'''_5474.py

BevelDifferentialPlanetGearCompoundHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import _5471
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_PLANET_GEAR_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound', 'BevelDifferentialPlanetGearCompoundHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialPlanetGearCompoundHarmonicAnalysisOfSingleExcitation',)


class BevelDifferentialPlanetGearCompoundHarmonicAnalysisOfSingleExcitation(_5471.BevelDifferentialGearCompoundHarmonicAnalysisOfSingleExcitation):
    '''BevelDifferentialPlanetGearCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_PLANET_GEAR_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialPlanetGearCompoundHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
