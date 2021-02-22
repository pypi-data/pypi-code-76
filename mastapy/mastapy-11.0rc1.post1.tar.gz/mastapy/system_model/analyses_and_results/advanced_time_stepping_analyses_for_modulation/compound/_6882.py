'''_6882.py

StraightBevelPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6876
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_PLANET_GEAR_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'StraightBevelPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation',)


class StraightBevelPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation(_6876.StraightBevelDiffGearCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''StraightBevelPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_PLANET_GEAR_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
