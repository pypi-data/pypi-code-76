'''_4456.py

ShaftHubConnectionCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2269
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4326
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4396
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'ShaftHubConnectionCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionCompoundModalAnalysisAtAStiffness',)


class ShaftHubConnectionCompoundModalAnalysisAtAStiffness(_4396.ConnectorCompoundModalAnalysisAtAStiffness):
    '''ShaftHubConnectionCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionCompoundModalAnalysisAtAStiffness.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_4326.ShaftHubConnectionModalAnalysisAtAStiffness]':
        '''List[ShaftHubConnectionModalAnalysisAtAStiffness]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4326.ShaftHubConnectionModalAnalysisAtAStiffness))
        return value

    @property
    def component_modal_analysis_at_a_stiffness_load_cases(self) -> 'List[_4326.ShaftHubConnectionModalAnalysisAtAStiffness]':
        '''List[ShaftHubConnectionModalAnalysisAtAStiffness]: 'ComponentModalAnalysisAtAStiffnessLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisAtAStiffnessLoadCases, constructor.new(_4326.ShaftHubConnectionModalAnalysisAtAStiffness))
        return value

    @property
    def planetaries(self) -> 'List[ShaftHubConnectionCompoundModalAnalysisAtAStiffness]':
        '''List[ShaftHubConnectionCompoundModalAnalysisAtAStiffness]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftHubConnectionCompoundModalAnalysisAtAStiffness))
        return value
