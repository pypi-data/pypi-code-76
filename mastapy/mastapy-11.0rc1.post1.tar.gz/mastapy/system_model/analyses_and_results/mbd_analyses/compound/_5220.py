'''_5220.py

CouplingHalfCompoundMultibodyDynamicsAnalysis
'''


from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5258
from mastapy._internal.python_net import python_net_import

_COUPLING_HALF_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'CouplingHalfCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingHalfCompoundMultibodyDynamicsAnalysis',)


class CouplingHalfCompoundMultibodyDynamicsAnalysis(_5258.MountableComponentCompoundMultibodyDynamicsAnalysis):
    '''CouplingHalfCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _COUPLING_HALF_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingHalfCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
