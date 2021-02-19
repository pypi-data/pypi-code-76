'''_3634.py

MountableComponentCompoundStabilityAnalysis
'''


from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3582
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'MountableComponentCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MountableComponentCompoundStabilityAnalysis',)


class MountableComponentCompoundStabilityAnalysis(_3582.ComponentCompoundStabilityAnalysis):
    '''MountableComponentCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _MOUNTABLE_COMPONENT_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MountableComponentCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
