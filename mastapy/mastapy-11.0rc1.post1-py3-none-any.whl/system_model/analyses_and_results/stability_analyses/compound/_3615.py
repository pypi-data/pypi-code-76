'''_3615.py

GearCompoundStabilityAnalysis
'''


from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3634
from mastapy._internal.python_net import python_net_import

_GEAR_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'GearCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GearCompoundStabilityAnalysis',)


class GearCompoundStabilityAnalysis(_3634.MountableComponentCompoundStabilityAnalysis):
    '''GearCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _GEAR_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
