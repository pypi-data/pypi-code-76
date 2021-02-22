'''_4696.py

OilSealCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model import _2139
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4567
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4654
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'OilSealCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealCompoundModalAnalysisAtASpeed',)


class OilSealCompoundModalAnalysisAtASpeed(_4654.ConnectorCompoundModalAnalysisAtASpeed):
    '''OilSealCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2139.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2139.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4567.OilSealModalAnalysisAtASpeed]':
        '''List[OilSealModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4567.OilSealModalAnalysisAtASpeed))
        return value

    @property
    def component_modal_analysis_at_a_speed_load_cases(self) -> 'List[_4567.OilSealModalAnalysisAtASpeed]':
        '''List[OilSealModalAnalysisAtASpeed]: 'ComponentModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisAtASpeedLoadCases, constructor.new(_4567.OilSealModalAnalysisAtASpeed))
        return value
