'''_3616.py

GearMeshCompoundStabilityAnalysis
'''


from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3622
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'GearMeshCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshCompoundStabilityAnalysis',)


class GearMeshCompoundStabilityAnalysis(_3622.InterMountableComponentConnectionCompoundStabilityAnalysis):
    '''GearMeshCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
