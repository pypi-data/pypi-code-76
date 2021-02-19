'''_2628.py

RootAssemblySteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.part_model import _2074
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2639, _2547
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'RootAssemblySteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblySteadyStateSynchronousResponseOnAShaft',)


class RootAssemblySteadyStateSynchronousResponseOnAShaft(_2547.AssemblySteadyStateSynchronousResponseOnAShaft):
    '''RootAssemblySteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblySteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2074.RootAssembly':
        '''RootAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2074.RootAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def steady_state_synchronous_response_on_a_shaft_inputs(self) -> '_2639.SteadyStateSynchronousResponseOnAShaft':
        '''SteadyStateSynchronousResponseOnAShaft: 'SteadyStateSynchronousResponseOnAShaftInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2639.SteadyStateSynchronousResponseOnAShaft)(self.wrapped.SteadyStateSynchronousResponseOnAShaftInputs) if self.wrapped.SteadyStateSynchronousResponseOnAShaftInputs else None
