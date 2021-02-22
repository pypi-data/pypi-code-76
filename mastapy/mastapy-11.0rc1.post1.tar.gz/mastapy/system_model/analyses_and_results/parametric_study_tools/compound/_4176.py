'''_4176.py

MassDiscCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _2135
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4036
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4223
from mastapy._internal.python_net import python_net_import

_MASS_DISC_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'MassDiscCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('MassDiscCompoundParametricStudyTool',)


class MassDiscCompoundParametricStudyTool(_4223.VirtualComponentCompoundParametricStudyTool):
    '''MassDiscCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _MASS_DISC_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MassDiscCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2135.MassDisc':
        '''MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2135.MassDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4036.MassDiscParametricStudyTool]':
        '''List[MassDiscParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4036.MassDiscParametricStudyTool))
        return value

    @property
    def component_parametric_study_tool_load_cases(self) -> 'List[_4036.MassDiscParametricStudyTool]':
        '''List[MassDiscParametricStudyTool]: 'ComponentParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentParametricStudyToolLoadCases, constructor.new(_4036.MassDiscParametricStudyTool))
        return value

    @property
    def planetaries(self) -> 'List[MassDiscCompoundParametricStudyTool]':
        '''List[MassDiscCompoundParametricStudyTool]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(MassDiscCompoundParametricStudyTool))
        return value
