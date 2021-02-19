'''_3594.py

CouplingCompoundStabilityAnalysis
'''


from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3655
from mastapy._internal.python_net import python_net_import

_COUPLING_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'CouplingCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingCompoundStabilityAnalysis',)


class CouplingCompoundStabilityAnalysis(_3655.SpecialisedAssemblyCompoundStabilityAnalysis):
    '''CouplingCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _COUPLING_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
