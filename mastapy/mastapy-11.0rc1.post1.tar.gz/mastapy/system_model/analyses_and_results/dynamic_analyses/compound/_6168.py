'''_6168.py

ZerolBevelGearCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2224
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6039
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6058
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'ZerolBevelGearCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearCompoundDynamicAnalysis',)


class ZerolBevelGearCompoundDynamicAnalysis(_6058.BevelGearCompoundDynamicAnalysis):
    '''ZerolBevelGearCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2224.ZerolBevelGear':
        '''ZerolBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2224.ZerolBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6039.ZerolBevelGearDynamicAnalysis]':
        '''List[ZerolBevelGearDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6039.ZerolBevelGearDynamicAnalysis))
        return value

    @property
    def component_dynamic_analysis_load_cases(self) -> 'List[_6039.ZerolBevelGearDynamicAnalysis]':
        '''List[ZerolBevelGearDynamicAnalysis]: 'ComponentDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDynamicAnalysisLoadCases, constructor.new(_6039.ZerolBevelGearDynamicAnalysis))
        return value
