'''_4211.py

StraightBevelGearSetCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2219
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4209, _4210, _4119
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4082
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'StraightBevelGearSetCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetCompoundParametricStudyTool',)


class StraightBevelGearSetCompoundParametricStudyTool(_4119.BevelGearSetCompoundParametricStudyTool):
    '''StraightBevelGearSetCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2219.StraightBevelGearSet':
        '''StraightBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2219.StraightBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2219.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2219.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def straight_bevel_gears_compound_parametric_study_tool(self) -> 'List[_4209.StraightBevelGearCompoundParametricStudyTool]':
        '''List[StraightBevelGearCompoundParametricStudyTool]: 'StraightBevelGearsCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsCompoundParametricStudyTool, constructor.new(_4209.StraightBevelGearCompoundParametricStudyTool))
        return value

    @property
    def straight_bevel_meshes_compound_parametric_study_tool(self) -> 'List[_4210.StraightBevelGearMeshCompoundParametricStudyTool]':
        '''List[StraightBevelGearMeshCompoundParametricStudyTool]: 'StraightBevelMeshesCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesCompoundParametricStudyTool, constructor.new(_4210.StraightBevelGearMeshCompoundParametricStudyTool))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4082.StraightBevelGearSetParametricStudyTool]':
        '''List[StraightBevelGearSetParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4082.StraightBevelGearSetParametricStudyTool))
        return value

    @property
    def assembly_parametric_study_tool_load_cases(self) -> 'List[_4082.StraightBevelGearSetParametricStudyTool]':
        '''List[StraightBevelGearSetParametricStudyTool]: 'AssemblyParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyParametricStudyToolLoadCases, constructor.new(_4082.StraightBevelGearSetParametricStudyTool))
        return value
