'''_3323.py

ConceptCouplingConnectionCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _2020
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3189
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _3334
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'ConceptCouplingConnectionCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingConnectionCompoundSteadyStateSynchronousResponse',)


class ConceptCouplingConnectionCompoundSteadyStateSynchronousResponse(_3334.CouplingConnectionCompoundSteadyStateSynchronousResponse):
    '''ConceptCouplingConnectionCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingConnectionCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2020.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2020.ConceptCouplingConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2020.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2020.ConceptCouplingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3189.ConceptCouplingConnectionSteadyStateSynchronousResponse]':
        '''List[ConceptCouplingConnectionSteadyStateSynchronousResponse]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3189.ConceptCouplingConnectionSteadyStateSynchronousResponse))
        return value

    @property
    def connection_steady_state_synchronous_response_load_cases(self) -> 'List[_3189.ConceptCouplingConnectionSteadyStateSynchronousResponse]':
        '''List[ConceptCouplingConnectionSteadyStateSynchronousResponse]: 'ConnectionSteadyStateSynchronousResponseLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSteadyStateSynchronousResponseLoadCases, constructor.new(_3189.ConceptCouplingConnectionSteadyStateSynchronousResponse))
        return value
