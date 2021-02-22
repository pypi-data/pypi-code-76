'''_4687.py

KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2209
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4559
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4684
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysisAtASpeed',)


class KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysisAtASpeed(_4684.KlingelnbergCycloPalloidConicalGearCompoundModalAnalysisAtASpeed):
    '''KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2209.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2209.KlingelnbergCycloPalloidHypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4559.KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed]':
        '''List[KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4559.KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed))
        return value

    @property
    def component_modal_analysis_at_a_speed_load_cases(self) -> 'List[_4559.KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed]':
        '''List[KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed]: 'ComponentModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisAtASpeedLoadCases, constructor.new(_4559.KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed))
        return value
