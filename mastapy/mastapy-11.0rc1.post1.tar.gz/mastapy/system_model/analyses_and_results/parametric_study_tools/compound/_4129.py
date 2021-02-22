'''_4129.py

ConceptCouplingHalfCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2253
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3981
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4140
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_HALF_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'ConceptCouplingHalfCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingHalfCompoundParametricStudyTool',)


class ConceptCouplingHalfCompoundParametricStudyTool(_4140.CouplingHalfCompoundParametricStudyTool):
    '''ConceptCouplingHalfCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_HALF_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingHalfCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2253.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2253.ConceptCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3981.ConceptCouplingHalfParametricStudyTool]':
        '''List[ConceptCouplingHalfParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3981.ConceptCouplingHalfParametricStudyTool))
        return value

    @property
    def component_parametric_study_tool_load_cases(self) -> 'List[_3981.ConceptCouplingHalfParametricStudyTool]':
        '''List[ConceptCouplingHalfParametricStudyTool]: 'ComponentParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentParametricStudyToolLoadCases, constructor.new(_3981.ConceptCouplingHalfParametricStudyTool))
        return value
