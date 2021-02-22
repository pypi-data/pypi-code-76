'''_6419.py

StraightBevelPlanetGearCompoundCriticalSpeedAnalysis
'''


from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6413
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_PLANET_GEAR_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'StraightBevelPlanetGearCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelPlanetGearCompoundCriticalSpeedAnalysis',)


class StraightBevelPlanetGearCompoundCriticalSpeedAnalysis(_6413.StraightBevelDiffGearCompoundCriticalSpeedAnalysis):
    '''StraightBevelPlanetGearCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_PLANET_GEAR_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelPlanetGearCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
