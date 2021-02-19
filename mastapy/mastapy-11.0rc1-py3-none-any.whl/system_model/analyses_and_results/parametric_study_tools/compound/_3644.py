'''_3644.py

ClutchCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2135
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3508
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3660
from mastapy._internal.python_net import python_net_import

_CLUTCH_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'ClutchCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchCompoundParametricStudyTool',)


class ClutchCompoundParametricStudyTool(_3660.CouplingCompoundParametricStudyTool):
    '''ClutchCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2135.Clutch':
        '''Clutch: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2135.Clutch)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2135.Clutch':
        '''Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2135.Clutch)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3508.ClutchParametricStudyTool]':
        '''List[ClutchParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3508.ClutchParametricStudyTool))
        return value

    @property
    def assembly_parametric_study_tool_load_cases(self) -> 'List[_3508.ClutchParametricStudyTool]':
        '''List[ClutchParametricStudyTool]: 'AssemblyParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyParametricStudyToolLoadCases, constructor.new(_3508.ClutchParametricStudyTool))
        return value
