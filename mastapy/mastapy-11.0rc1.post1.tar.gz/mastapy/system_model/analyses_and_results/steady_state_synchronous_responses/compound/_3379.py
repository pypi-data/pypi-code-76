'''_3379.py

PlanetaryConnectionCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1963
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3247
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _3393
from mastapy._internal.python_net import python_net_import

_PLANETARY_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'PlanetaryConnectionCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryConnectionCompoundSteadyStateSynchronousResponse',)


class PlanetaryConnectionCompoundSteadyStateSynchronousResponse(_3393.ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponse):
    '''PlanetaryConnectionCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryConnectionCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1963.PlanetaryConnection':
        '''PlanetaryConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1963.PlanetaryConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1963.PlanetaryConnection':
        '''PlanetaryConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1963.PlanetaryConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3247.PlanetaryConnectionSteadyStateSynchronousResponse]':
        '''List[PlanetaryConnectionSteadyStateSynchronousResponse]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3247.PlanetaryConnectionSteadyStateSynchronousResponse))
        return value

    @property
    def connection_steady_state_synchronous_response_load_cases(self) -> 'List[_3247.PlanetaryConnectionSteadyStateSynchronousResponse]':
        '''List[PlanetaryConnectionSteadyStateSynchronousResponse]: 'ConnectionSteadyStateSynchronousResponseLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSteadyStateSynchronousResponseLoadCases, constructor.new(_3247.PlanetaryConnectionSteadyStateSynchronousResponse))
        return value
