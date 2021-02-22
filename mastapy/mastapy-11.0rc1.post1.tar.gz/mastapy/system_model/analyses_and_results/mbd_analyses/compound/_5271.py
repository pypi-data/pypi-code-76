'''_5271.py

RingPinsToDiscConnectionCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.cycloidal import _2017
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5130
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5246
from mastapy._internal.python_net import python_net_import

_RING_PINS_TO_DISC_CONNECTION_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'RingPinsToDiscConnectionCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsToDiscConnectionCompoundMultibodyDynamicsAnalysis',)


class RingPinsToDiscConnectionCompoundMultibodyDynamicsAnalysis(_5246.InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis):
    '''RingPinsToDiscConnectionCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_TO_DISC_CONNECTION_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsToDiscConnectionCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2017.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2017.RingPinsToDiscConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2017.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2017.RingPinsToDiscConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5130.RingPinsToDiscConnectionMultibodyDynamicsAnalysis]':
        '''List[RingPinsToDiscConnectionMultibodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5130.RingPinsToDiscConnectionMultibodyDynamicsAnalysis))
        return value

    @property
    def connection_multibody_dynamics_analysis_load_cases(self) -> 'List[_5130.RingPinsToDiscConnectionMultibodyDynamicsAnalysis]':
        '''List[RingPinsToDiscConnectionMultibodyDynamicsAnalysis]: 'ConnectionMultibodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionMultibodyDynamicsAnalysisLoadCases, constructor.new(_5130.RingPinsToDiscConnectionMultibodyDynamicsAnalysis))
        return value
