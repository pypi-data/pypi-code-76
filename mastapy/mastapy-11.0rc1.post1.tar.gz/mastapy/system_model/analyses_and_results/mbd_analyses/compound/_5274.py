'''_5274.py

RollingRingConnectionCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1968
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5132
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5246
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_CONNECTION_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'RollingRingConnectionCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingConnectionCompoundMultibodyDynamicsAnalysis',)


class RollingRingConnectionCompoundMultibodyDynamicsAnalysis(_5246.InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis):
    '''RollingRingConnectionCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_CONNECTION_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingConnectionCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1968.RollingRingConnection':
        '''RollingRingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1968.RollingRingConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1968.RollingRingConnection':
        '''RollingRingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1968.RollingRingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5132.RollingRingConnectionMultibodyDynamicsAnalysis]':
        '''List[RollingRingConnectionMultibodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5132.RollingRingConnectionMultibodyDynamicsAnalysis))
        return value

    @property
    def connection_multibody_dynamics_analysis_load_cases(self) -> 'List[_5132.RollingRingConnectionMultibodyDynamicsAnalysis]':
        '''List[RollingRingConnectionMultibodyDynamicsAnalysis]: 'ConnectionMultibodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionMultibodyDynamicsAnalysisLoadCases, constructor.new(_5132.RollingRingConnectionMultibodyDynamicsAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[RollingRingConnectionCompoundMultibodyDynamicsAnalysis]':
        '''List[RollingRingConnectionCompoundMultibodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingConnectionCompoundMultibodyDynamicsAnalysis))
        return value
