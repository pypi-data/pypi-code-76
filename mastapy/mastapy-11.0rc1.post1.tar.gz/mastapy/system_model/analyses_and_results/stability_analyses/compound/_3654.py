'''_3654.py

ShaftToMountableComponentConnectionCompoundStabilityAnalysis
'''


from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3560
from mastapy._internal.python_net import python_net_import

_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'ShaftToMountableComponentConnectionCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftToMountableComponentConnectionCompoundStabilityAnalysis',)


class ShaftToMountableComponentConnectionCompoundStabilityAnalysis(_3560.AbstractShaftToMountableComponentConnectionCompoundStabilityAnalysis):
    '''ShaftToMountableComponentConnectionCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftToMountableComponentConnectionCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
