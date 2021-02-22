'''_3571.py

BevelDifferentialPlanetGearCompoundStabilityAnalysis
'''


from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3568
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_PLANET_GEAR_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'BevelDifferentialPlanetGearCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialPlanetGearCompoundStabilityAnalysis',)


class BevelDifferentialPlanetGearCompoundStabilityAnalysis(_3568.BevelDifferentialGearCompoundStabilityAnalysis):
    '''BevelDifferentialPlanetGearCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_PLANET_GEAR_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialPlanetGearCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
