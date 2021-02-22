'''_4726.py

StraightBevelGearCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2218
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4598
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4634
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'StraightBevelGearCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearCompoundModalAnalysisAtASpeed',)


class StraightBevelGearCompoundModalAnalysisAtASpeed(_4634.BevelGearCompoundModalAnalysisAtASpeed):
    '''StraightBevelGearCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2218.StraightBevelGear':
        '''StraightBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2218.StraightBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4598.StraightBevelGearModalAnalysisAtASpeed]':
        '''List[StraightBevelGearModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4598.StraightBevelGearModalAnalysisAtASpeed))
        return value

    @property
    def component_modal_analysis_at_a_speed_load_cases(self) -> 'List[_4598.StraightBevelGearModalAnalysisAtASpeed]':
        '''List[StraightBevelGearModalAnalysisAtASpeed]: 'ComponentModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisAtASpeedLoadCases, constructor.new(_4598.StraightBevelGearModalAnalysisAtASpeed))
        return value
