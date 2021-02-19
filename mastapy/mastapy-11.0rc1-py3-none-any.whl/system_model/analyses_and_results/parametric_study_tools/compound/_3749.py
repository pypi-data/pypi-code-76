'''_3749.py

RollingRingCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2190
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3629
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3702
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'RollingRingCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingCompoundParametricStudyTool',)


class RollingRingCompoundParametricStudyTool(_3702.CouplingHalfCompoundParametricStudyTool):
    '''RollingRingCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2190.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2190.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3629.RollingRingParametricStudyTool]':
        '''List[RollingRingParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3629.RollingRingParametricStudyTool))
        return value

    @property
    def component_parametric_study_tool_load_cases(self) -> 'List[_3629.RollingRingParametricStudyTool]':
        '''List[RollingRingParametricStudyTool]: 'ComponentParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentParametricStudyToolLoadCases, constructor.new(_3629.RollingRingParametricStudyTool))
        return value

    @property
    def planetaries(self) -> 'List[RollingRingCompoundParametricStudyTool]':
        '''List[RollingRingCompoundParametricStudyTool]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingCompoundParametricStudyTool))
        return value
