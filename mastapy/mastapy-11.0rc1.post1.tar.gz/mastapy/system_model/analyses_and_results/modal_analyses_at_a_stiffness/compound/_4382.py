'''_4382.py

ClutchConnectionCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _2018
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4251
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4398
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'ClutchConnectionCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionCompoundModalAnalysisAtAStiffness',)


class ClutchConnectionCompoundModalAnalysisAtAStiffness(_4398.CouplingConnectionCompoundModalAnalysisAtAStiffness):
    '''ClutchConnectionCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2018.ClutchConnection':
        '''ClutchConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2018.ClutchConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2018.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2018.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4251.ClutchConnectionModalAnalysisAtAStiffness]':
        '''List[ClutchConnectionModalAnalysisAtAStiffness]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4251.ClutchConnectionModalAnalysisAtAStiffness))
        return value

    @property
    def connection_modal_analysis_at_a_stiffness_load_cases(self) -> 'List[_4251.ClutchConnectionModalAnalysisAtAStiffness]':
        '''List[ClutchConnectionModalAnalysisAtAStiffness]: 'ConnectionModalAnalysisAtAStiffnessLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysisAtAStiffnessLoadCases, constructor.new(_4251.ClutchConnectionModalAnalysisAtAStiffness))
        return value
