'''_5206.py

ComponentCompoundMultibodyDynamicsAnalysis
'''


from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5260
from mastapy._internal.python_net import python_net_import

_COMPONENT_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'ComponentCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentCompoundMultibodyDynamicsAnalysis',)


class ComponentCompoundMultibodyDynamicsAnalysis(_5260.PartCompoundMultibodyDynamicsAnalysis):
    '''ComponentCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPONENT_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
