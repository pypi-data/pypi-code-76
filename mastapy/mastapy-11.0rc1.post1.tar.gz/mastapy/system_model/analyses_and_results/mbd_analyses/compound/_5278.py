'''_5278.py

ShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis
'''


from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5184
from mastapy._internal.python_net import python_net_import

_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'ShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis',)


class ShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis(_5184.AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis):
    '''ShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
