'''_5218.py

CouplingCompoundMultibodyDynamicsAnalysis
'''


from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5279
from mastapy._internal.python_net import python_net_import

_COUPLING_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'CouplingCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingCompoundMultibodyDynamicsAnalysis',)


class CouplingCompoundMultibodyDynamicsAnalysis(_5279.SpecialisedAssemblyCompoundMultibodyDynamicsAnalysis):
    '''CouplingCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _COUPLING_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
