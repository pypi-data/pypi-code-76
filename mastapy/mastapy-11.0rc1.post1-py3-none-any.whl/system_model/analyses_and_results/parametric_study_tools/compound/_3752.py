'''_3752.py

ShaftCompoundParametricStudyTool
'''


from typing import List

from mastapy.shafts import _18
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.shaft_model import _2081
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3632
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3666
from mastapy._internal.python_net import python_net_import

_SHAFT_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'ShaftCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftCompoundParametricStudyTool',)


class ShaftCompoundParametricStudyTool(_3666.AbstractShaftOrHousingCompoundParametricStudyTool):
    '''ShaftCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _SHAFT_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def shaft_duty_cycle_results(self) -> '_18.ShaftDamageResults':
        '''ShaftDamageResults: 'ShaftDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_18.ShaftDamageResults)(self.wrapped.ShaftDutyCycleResults) if self.wrapped.ShaftDutyCycleResults else None

    @property
    def component_design(self) -> '_2081.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2081.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3632.ShaftParametricStudyTool]':
        '''List[ShaftParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3632.ShaftParametricStudyTool))
        return value

    @property
    def component_parametric_study_tool_load_cases(self) -> 'List[_3632.ShaftParametricStudyTool]':
        '''List[ShaftParametricStudyTool]: 'ComponentParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentParametricStudyToolLoadCases, constructor.new(_3632.ShaftParametricStudyTool))
        return value

    @property
    def planetaries(self) -> 'List[ShaftCompoundParametricStudyTool]':
        '''List[ShaftCompoundParametricStudyTool]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftCompoundParametricStudyTool))
        return value
