'''_6312.py

AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis
'''


from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6340
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis',)


class AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis(_6340.ConicalGearCompoundCriticalSpeedAnalysis):
    '''AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
