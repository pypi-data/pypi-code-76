'''_3665.py

StraightBevelGearCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2218
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3538
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3573
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'StraightBevelGearCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearCompoundStabilityAnalysis',)


class StraightBevelGearCompoundStabilityAnalysis(_3573.BevelGearCompoundStabilityAnalysis):
    '''StraightBevelGearCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2218.StraightBevelGear':
        '''StraightBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2218.StraightBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3538.StraightBevelGearStabilityAnalysis]':
        '''List[StraightBevelGearStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3538.StraightBevelGearStabilityAnalysis))
        return value

    @property
    def component_stability_analysis_load_cases(self) -> 'List[_3538.StraightBevelGearStabilityAnalysis]':
        '''List[StraightBevelGearStabilityAnalysis]: 'ComponentStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentStabilityAnalysisLoadCases, constructor.new(_3538.StraightBevelGearStabilityAnalysis))
        return value
