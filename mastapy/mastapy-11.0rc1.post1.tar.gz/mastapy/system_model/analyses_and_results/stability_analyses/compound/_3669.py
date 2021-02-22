'''_3669.py

StraightBevelSunGearCompoundStabilityAnalysis
'''


from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3662
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_SUN_GEAR_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'StraightBevelSunGearCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelSunGearCompoundStabilityAnalysis',)


class StraightBevelSunGearCompoundStabilityAnalysis(_3662.StraightBevelDiffGearCompoundStabilityAnalysis):
    '''StraightBevelSunGearCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_SUN_GEAR_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelSunGearCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
