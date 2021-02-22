'''_5186.py

AGMAGleasonConicalGearMeshCompoundMultibodyDynamicsAnalysis
'''


from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5214
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'AGMAGleasonConicalGearMeshCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGearMeshCompoundMultibodyDynamicsAnalysis',)


class AGMAGleasonConicalGearMeshCompoundMultibodyDynamicsAnalysis(_5214.ConicalGearMeshCompoundMultibodyDynamicsAnalysis):
    '''AGMAGleasonConicalGearMeshCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalGearMeshCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
