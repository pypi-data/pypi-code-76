'''_4440.py

PartToPartShearCouplingCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2259
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4313
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4397
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'PartToPartShearCouplingCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingCompoundModalAnalysisAtAStiffness',)


class PartToPartShearCouplingCompoundModalAnalysisAtAStiffness(_4397.CouplingCompoundModalAnalysisAtAStiffness):
    '''PartToPartShearCouplingCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2259.PartToPartShearCoupling':
        '''PartToPartShearCoupling: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2259.PartToPartShearCoupling)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2259.PartToPartShearCoupling':
        '''PartToPartShearCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2259.PartToPartShearCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4313.PartToPartShearCouplingModalAnalysisAtAStiffness]':
        '''List[PartToPartShearCouplingModalAnalysisAtAStiffness]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4313.PartToPartShearCouplingModalAnalysisAtAStiffness))
        return value

    @property
    def assembly_modal_analysis_at_a_stiffness_load_cases(self) -> 'List[_4313.PartToPartShearCouplingModalAnalysisAtAStiffness]':
        '''List[PartToPartShearCouplingModalAnalysisAtAStiffness]: 'AssemblyModalAnalysisAtAStiffnessLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisAtAStiffnessLoadCases, constructor.new(_4313.PartToPartShearCouplingModalAnalysisAtAStiffness))
        return value
