'''_6358.py

CylindricalPlanetGearCompoundCriticalSpeedAnalysis
'''


from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6355
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANET_GEAR_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'CylindricalPlanetGearCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalPlanetGearCompoundCriticalSpeedAnalysis',)


class CylindricalPlanetGearCompoundCriticalSpeedAnalysis(_6355.CylindricalGearCompoundCriticalSpeedAnalysis):
    '''CylindricalPlanetGearCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_PLANET_GEAR_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalPlanetGearCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
