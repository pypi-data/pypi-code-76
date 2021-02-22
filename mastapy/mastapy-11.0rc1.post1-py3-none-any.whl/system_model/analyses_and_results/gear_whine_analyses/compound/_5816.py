'''_5816.py

PowerLoadCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2072
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5423
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5849
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'PowerLoadCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadCompoundGearWhineAnalysis',)


class PowerLoadCompoundGearWhineAnalysis(_5849.VirtualComponentCompoundGearWhineAnalysis):
    '''PowerLoadCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoadCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2072.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2072.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5423.PowerLoadGearWhineAnalysis]':
        '''List[PowerLoadGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5423.PowerLoadGearWhineAnalysis))
        return value

    @property
    def component_gear_whine_analysis_load_cases(self) -> 'List[_5423.PowerLoadGearWhineAnalysis]':
        '''List[PowerLoadGearWhineAnalysis]: 'ComponentGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentGearWhineAnalysisLoadCases, constructor.new(_5423.PowerLoadGearWhineAnalysis))
        return value
