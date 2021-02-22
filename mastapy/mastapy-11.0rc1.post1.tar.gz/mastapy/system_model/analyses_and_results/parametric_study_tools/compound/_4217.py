'''_4217.py

SynchroniserSleeveCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2277
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4088
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4216
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_SLEEVE_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'SynchroniserSleeveCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserSleeveCompoundParametricStudyTool',)


class SynchroniserSleeveCompoundParametricStudyTool(_4216.SynchroniserPartCompoundParametricStudyTool):
    '''SynchroniserSleeveCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_SLEEVE_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserSleeveCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2277.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2277.SynchroniserSleeve)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4088.SynchroniserSleeveParametricStudyTool]':
        '''List[SynchroniserSleeveParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4088.SynchroniserSleeveParametricStudyTool))
        return value

    @property
    def component_parametric_study_tool_load_cases(self) -> 'List[_4088.SynchroniserSleeveParametricStudyTool]':
        '''List[SynchroniserSleeveParametricStudyTool]: 'ComponentParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentParametricStudyToolLoadCases, constructor.new(_4088.SynchroniserSleeveParametricStudyTool))
        return value
