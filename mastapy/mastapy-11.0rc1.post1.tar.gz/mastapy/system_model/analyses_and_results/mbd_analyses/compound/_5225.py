'''_5225.py

CycloidalDiscCentralBearingConnectionCompoundMultibodyDynamicsAnalysis
'''


from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5205
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'CycloidalDiscCentralBearingConnectionCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscCentralBearingConnectionCompoundMultibodyDynamicsAnalysis',)


class CycloidalDiscCentralBearingConnectionCompoundMultibodyDynamicsAnalysis(_5205.CoaxialConnectionCompoundMultibodyDynamicsAnalysis):
    '''CycloidalDiscCentralBearingConnectionCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscCentralBearingConnectionCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
