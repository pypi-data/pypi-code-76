'''_4422.py

HypoidGearCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.gears import _2205
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4294
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4364
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'HypoidGearCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearCompoundModalAnalysisAtAStiffness',)


class HypoidGearCompoundModalAnalysisAtAStiffness(_4364.AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness):
    '''HypoidGearCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2205.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2205.HypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4294.HypoidGearModalAnalysisAtAStiffness]':
        '''List[HypoidGearModalAnalysisAtAStiffness]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4294.HypoidGearModalAnalysisAtAStiffness))
        return value

    @property
    def component_modal_analysis_at_a_stiffness_load_cases(self) -> 'List[_4294.HypoidGearModalAnalysisAtAStiffness]':
        '''List[HypoidGearModalAnalysisAtAStiffness]: 'ComponentModalAnalysisAtAStiffnessLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisAtAStiffnessLoadCases, constructor.new(_4294.HypoidGearModalAnalysisAtAStiffness))
        return value
