'''_4694.py

MeasurementComponentCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model import _2136
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4565
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4740
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'MeasurementComponentCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentCompoundModalAnalysisAtASpeed',)


class MeasurementComponentCompoundModalAnalysisAtASpeed(_4740.VirtualComponentCompoundModalAnalysisAtASpeed):
    '''MeasurementComponentCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_COMPONENT_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementComponentCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2136.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2136.MeasurementComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4565.MeasurementComponentModalAnalysisAtASpeed]':
        '''List[MeasurementComponentModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4565.MeasurementComponentModalAnalysisAtASpeed))
        return value

    @property
    def component_modal_analysis_at_a_speed_load_cases(self) -> 'List[_4565.MeasurementComponentModalAnalysisAtASpeed]':
        '''List[MeasurementComponentModalAnalysisAtASpeed]: 'ComponentModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisAtASpeedLoadCases, constructor.new(_4565.MeasurementComponentModalAnalysisAtASpeed))
        return value
