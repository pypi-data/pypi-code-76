'''_4711.py

RollingRingConnectionCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1968
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4581
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4683
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'RollingRingConnectionCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingConnectionCompoundModalAnalysisAtASpeed',)


class RollingRingConnectionCompoundModalAnalysisAtASpeed(_4683.InterMountableComponentConnectionCompoundModalAnalysisAtASpeed):
    '''RollingRingConnectionCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingConnectionCompoundModalAnalysisAtASpeed.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_4581.RollingRingConnectionModalAnalysisAtASpeed]':
        '''List[RollingRingConnectionModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4581.RollingRingConnectionModalAnalysisAtASpeed))
        return value

    @property
    def connection_modal_analysis_at_a_speed_load_cases(self) -> 'List[_4581.RollingRingConnectionModalAnalysisAtASpeed]':
        '''List[RollingRingConnectionModalAnalysisAtASpeed]: 'ConnectionModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysisAtASpeedLoadCases, constructor.new(_4581.RollingRingConnectionModalAnalysisAtASpeed))
        return value

    @property
    def planetaries(self) -> 'List[RollingRingConnectionCompoundModalAnalysisAtASpeed]':
        '''List[RollingRingConnectionCompoundModalAnalysisAtASpeed]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingConnectionCompoundModalAnalysisAtASpeed))
        return value
