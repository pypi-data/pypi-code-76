'''_5756.py

ClutchHalfCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2173
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5340
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5772
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'ClutchHalfCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalfCompoundGearWhineAnalysis',)


class ClutchHalfCompoundGearWhineAnalysis(_5772.CouplingHalfCompoundGearWhineAnalysis):
    '''ClutchHalfCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_HALF_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchHalfCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2173.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2173.ClutchHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5340.ClutchHalfGearWhineAnalysis]':
        '''List[ClutchHalfGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5340.ClutchHalfGearWhineAnalysis))
        return value

    @property
    def component_gear_whine_analysis_load_cases(self) -> 'List[_5340.ClutchHalfGearWhineAnalysis]':
        '''List[ClutchHalfGearWhineAnalysis]: 'ComponentGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentGearWhineAnalysisLoadCases, constructor.new(_5340.ClutchHalfGearWhineAnalysis))
        return value
