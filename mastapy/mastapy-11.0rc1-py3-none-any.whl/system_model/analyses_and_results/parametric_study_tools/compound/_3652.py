'''_3652.py

BearingCompoundParametricStudyTool
'''


from typing import List

from mastapy.bearings.bearing_results import _1603, _1611, _1614
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.bearings.bearing_results.rolling import (
    _1640, _1647, _1655, _1671,
    _1695
)
from mastapy.system_model.part_model import _2026
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3514
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3680
from mastapy._internal.python_net import python_net_import

_BEARING_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'BearingCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingCompoundParametricStudyTool',)


class BearingCompoundParametricStudyTool(_3680.ConnectorCompoundParametricStudyTool):
    '''BearingCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _BEARING_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bearing_duty_cycle_results(self) -> '_1603.LoadedBearingDutyCycle':
        '''LoadedBearingDutyCycle: 'BearingDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1603.LoadedBearingDutyCycle.TYPE not in self.wrapped.BearingDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast bearing_duty_cycle_results to LoadedBearingDutyCycle. Expected: {}.'.format(self.wrapped.BearingDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDutyCycleResults.__class__)(self.wrapped.BearingDutyCycleResults) if self.wrapped.BearingDutyCycleResults else None

    @property
    def component_design(self) -> '_2026.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2026.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3514.BearingParametricStudyTool]':
        '''List[BearingParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3514.BearingParametricStudyTool))
        return value

    @property
    def component_parametric_study_tool_load_cases(self) -> 'List[_3514.BearingParametricStudyTool]':
        '''List[BearingParametricStudyTool]: 'ComponentParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentParametricStudyToolLoadCases, constructor.new(_3514.BearingParametricStudyTool))
        return value

    @property
    def planetaries(self) -> 'List[BearingCompoundParametricStudyTool]':
        '''List[BearingCompoundParametricStudyTool]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingCompoundParametricStudyTool))
        return value
