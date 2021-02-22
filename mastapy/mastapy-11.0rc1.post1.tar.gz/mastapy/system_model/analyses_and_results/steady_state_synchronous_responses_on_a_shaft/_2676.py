'''_2676.py

ConceptGearSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.part_model.gears import _2192
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6472
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2705
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'ConceptGearSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSteadyStateSynchronousResponseOnAShaft',)


class ConceptGearSteadyStateSynchronousResponseOnAShaft(_2705.GearSteadyStateSynchronousResponseOnAShaft):
    '''ConceptGearSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2192.ConceptGear':
        '''ConceptGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2192.ConceptGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6472.ConceptGearLoadCase':
        '''ConceptGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6472.ConceptGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
