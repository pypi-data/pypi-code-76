'''_5187.py

AGMAGleasonConicalGearSetCompoundMultibodyDynamicsAnalysis
'''


from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5215
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_SET_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'AGMAGleasonConicalGearSetCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGearSetCompoundMultibodyDynamicsAnalysis',)


class AGMAGleasonConicalGearSetCompoundMultibodyDynamicsAnalysis(_5215.ConicalGearSetCompoundMultibodyDynamicsAnalysis):
    '''AGMAGleasonConicalGearSetCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_SET_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalGearSetCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
