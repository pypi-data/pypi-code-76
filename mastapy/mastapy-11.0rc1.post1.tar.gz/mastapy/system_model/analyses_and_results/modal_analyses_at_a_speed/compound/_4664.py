'''_4664.py

CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.connections_and_sockets.cycloidal import _2014
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4535
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4621
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysisAtASpeed',)


class CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysisAtASpeed(_4621.AbstractShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed):
    '''CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2014.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2014.CycloidalDiscPlanetaryBearingConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2014.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2014.CycloidalDiscPlanetaryBearingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4535.CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtASpeed]':
        '''List[CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4535.CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtASpeed))
        return value

    @property
    def connection_modal_analysis_at_a_speed_load_cases(self) -> 'List[_4535.CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtASpeed]':
        '''List[CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtASpeed]: 'ConnectionModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysisAtASpeedLoadCases, constructor.new(_4535.CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtASpeed))
        return value
