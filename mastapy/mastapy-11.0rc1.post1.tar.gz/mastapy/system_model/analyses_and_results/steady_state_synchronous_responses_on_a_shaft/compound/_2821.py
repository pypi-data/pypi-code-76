'''_2821.py

CycloidalDiscPlanetaryBearingConnectionCompoundSteadyStateSynchronousResponseOnAShaft
'''


from typing import List

from mastapy.system_model.connections_and_sockets.cycloidal import _2014
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2690
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import _2778
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound', 'CycloidalDiscPlanetaryBearingConnectionCompoundSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscPlanetaryBearingConnectionCompoundSteadyStateSynchronousResponseOnAShaft',)


class CycloidalDiscPlanetaryBearingConnectionCompoundSteadyStateSynchronousResponseOnAShaft(_2778.AbstractShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft):
    '''CycloidalDiscPlanetaryBearingConnectionCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscPlanetaryBearingConnectionCompoundSteadyStateSynchronousResponseOnAShaft.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_2690.CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseOnAShaft]':
        '''List[CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseOnAShaft]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2690.CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def connection_steady_state_synchronous_response_on_a_shaft_load_cases(self) -> 'List[_2690.CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseOnAShaft]':
        '''List[CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseOnAShaft]: 'ConnectionSteadyStateSynchronousResponseOnAShaftLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSteadyStateSynchronousResponseOnAShaftLoadCases, constructor.new(_2690.CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseOnAShaft))
        return value
