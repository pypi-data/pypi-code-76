'''_3562.py

AGMAGleasonConicalGearMeshCompoundStabilityAnalysis
'''


from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3590
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'AGMAGleasonConicalGearMeshCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGearMeshCompoundStabilityAnalysis',)


class AGMAGleasonConicalGearMeshCompoundStabilityAnalysis(_3590.ConicalGearMeshCompoundStabilityAnalysis):
    '''AGMAGleasonConicalGearMeshCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalGearMeshCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
