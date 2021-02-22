'''_3390.py

RootAssemblyCompoundSteadyStateSynchronousResponse
'''


from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _3303
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'RootAssemblyCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyCompoundSteadyStateSynchronousResponse',)


class RootAssemblyCompoundSteadyStateSynchronousResponse(_3303.AssemblyCompoundSteadyStateSynchronousResponse):
    '''RootAssemblyCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblyCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
