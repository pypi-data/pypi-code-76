'''_3596.py

CouplingHalfCompoundStabilityAnalysis
'''


from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3634
from mastapy._internal.python_net import python_net_import

_COUPLING_HALF_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'CouplingHalfCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingHalfCompoundStabilityAnalysis',)


class CouplingHalfCompoundStabilityAnalysis(_3634.MountableComponentCompoundStabilityAnalysis):
    '''CouplingHalfCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _COUPLING_HALF_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingHalfCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
