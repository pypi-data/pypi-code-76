'''_3145.py

StraightBevelPlanetGearCompoundSteadyStateSynchronousResponseAtASpeed
'''


from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _3139
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_PLANET_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'StraightBevelPlanetGearCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelPlanetGearCompoundSteadyStateSynchronousResponseAtASpeed',)


class StraightBevelPlanetGearCompoundSteadyStateSynchronousResponseAtASpeed(_3139.StraightBevelDiffGearCompoundSteadyStateSynchronousResponseAtASpeed):
    '''StraightBevelPlanetGearCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_PLANET_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelPlanetGearCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
