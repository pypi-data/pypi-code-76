'''_2726.py

PartToPartShearCouplingHalfSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.part_model.couplings import _2260
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6559
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2683
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_HALF_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'PartToPartShearCouplingHalfSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingHalfSteadyStateSynchronousResponseOnAShaft',)


class PartToPartShearCouplingHalfSteadyStateSynchronousResponseOnAShaft(_2683.CouplingHalfSteadyStateSynchronousResponseOnAShaft):
    '''PartToPartShearCouplingHalfSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_HALF_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingHalfSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2260.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2260.PartToPartShearCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6559.PartToPartShearCouplingHalfLoadCase':
        '''PartToPartShearCouplingHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6559.PartToPartShearCouplingHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
