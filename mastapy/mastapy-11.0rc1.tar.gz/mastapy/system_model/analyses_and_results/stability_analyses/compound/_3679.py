'''_3679.py

VirtualComponentCompoundStabilityAnalysis
'''


from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3634
from mastapy._internal.python_net import python_net_import

_VIRTUAL_COMPONENT_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'VirtualComponentCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('VirtualComponentCompoundStabilityAnalysis',)


class VirtualComponentCompoundStabilityAnalysis(_3634.MountableComponentCompoundStabilityAnalysis):
    '''VirtualComponentCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _VIRTUAL_COMPONENT_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'VirtualComponentCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
