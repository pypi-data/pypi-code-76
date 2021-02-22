'''_3553.py

ComponentCompoundStabilityAnalysis
'''


from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3607
from mastapy._internal.python_net import python_net_import

_COMPONENT_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'ComponentCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentCompoundStabilityAnalysis',)


class ComponentCompoundStabilityAnalysis(_3607.PartCompoundStabilityAnalysis):
    '''ComponentCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPONENT_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
