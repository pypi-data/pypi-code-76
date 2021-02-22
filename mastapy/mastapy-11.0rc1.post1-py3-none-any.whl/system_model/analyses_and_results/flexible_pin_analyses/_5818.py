'''_5818.py

FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass
'''


from mastapy.system_model.analyses_and_results.flexible_pin_analyses import _5816
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ANALYSIS_DETAIL_LEVEL_AND_PIN_FATIGUE_ONE_TOOTH_PASS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.FlexiblePinAnalyses', 'FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass',)


class FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass(_5816.FlexiblePinAnalysis):
    '''FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass

    This is a mastapy class.
    '''

    TYPE = _FLEXIBLE_PIN_ANALYSIS_DETAIL_LEVEL_AND_PIN_FATIGUE_ONE_TOOTH_PASS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
