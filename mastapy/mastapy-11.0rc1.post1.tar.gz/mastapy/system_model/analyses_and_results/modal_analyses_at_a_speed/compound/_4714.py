'''_4714.py

ShaftHubConnectionCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2269
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4584
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4654
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'ShaftHubConnectionCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionCompoundModalAnalysisAtASpeed',)


class ShaftHubConnectionCompoundModalAnalysisAtASpeed(_4654.ConnectorCompoundModalAnalysisAtASpeed):
    '''ShaftHubConnectionCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2269.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2269.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4584.ShaftHubConnectionModalAnalysisAtASpeed]':
        '''List[ShaftHubConnectionModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4584.ShaftHubConnectionModalAnalysisAtASpeed))
        return value

    @property
    def component_modal_analysis_at_a_speed_load_cases(self) -> 'List[_4584.ShaftHubConnectionModalAnalysisAtASpeed]':
        '''List[ShaftHubConnectionModalAnalysisAtASpeed]: 'ComponentModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisAtASpeedLoadCases, constructor.new(_4584.ShaftHubConnectionModalAnalysisAtASpeed))
        return value

    @property
    def planetaries(self) -> 'List[ShaftHubConnectionCompoundModalAnalysisAtASpeed]':
        '''List[ShaftHubConnectionCompoundModalAnalysisAtASpeed]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftHubConnectionCompoundModalAnalysisAtASpeed))
        return value
