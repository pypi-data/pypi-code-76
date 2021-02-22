'''_4477.py

TorqueConverterCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2278
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4349
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4397
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'TorqueConverterCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterCompoundModalAnalysisAtAStiffness',)


class TorqueConverterCompoundModalAnalysisAtAStiffness(_4397.CouplingCompoundModalAnalysisAtAStiffness):
    '''TorqueConverterCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2278.TorqueConverter':
        '''TorqueConverter: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2278.TorqueConverter)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2278.TorqueConverter':
        '''TorqueConverter: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2278.TorqueConverter)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4349.TorqueConverterModalAnalysisAtAStiffness]':
        '''List[TorqueConverterModalAnalysisAtAStiffness]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4349.TorqueConverterModalAnalysisAtAStiffness))
        return value

    @property
    def assembly_modal_analysis_at_a_stiffness_load_cases(self) -> 'List[_4349.TorqueConverterModalAnalysisAtAStiffness]':
        '''List[TorqueConverterModalAnalysisAtAStiffness]: 'AssemblyModalAnalysisAtAStiffnessLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisAtAStiffnessLoadCases, constructor.new(_4349.TorqueConverterModalAnalysisAtAStiffness))
        return value
