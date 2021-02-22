'''_3203.py

CVTBeltConnectionSteadyStateSynchronousResponse
'''


from mastapy.system_model.connections_and_sockets import _1949
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3172
from mastapy._internal.python_net import python_net_import

_CVT_BELT_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'CVTBeltConnectionSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTBeltConnectionSteadyStateSynchronousResponse',)


class CVTBeltConnectionSteadyStateSynchronousResponse(_3172.BeltConnectionSteadyStateSynchronousResponse):
    '''CVTBeltConnectionSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _CVT_BELT_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTBeltConnectionSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1949.CVTBeltConnection':
        '''CVTBeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1949.CVTBeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None
