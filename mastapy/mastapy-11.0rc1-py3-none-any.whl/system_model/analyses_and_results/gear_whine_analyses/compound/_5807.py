'''_5807.py

OilSealCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2066
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5413
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5769
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'OilSealCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealCompoundGearWhineAnalysis',)


class OilSealCompoundGearWhineAnalysis(_5769.ConnectorCompoundGearWhineAnalysis):
    '''OilSealCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2066.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2066.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5413.OilSealGearWhineAnalysis]':
        '''List[OilSealGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5413.OilSealGearWhineAnalysis))
        return value

    @property
    def component_gear_whine_analysis_load_cases(self) -> 'List[_5413.OilSealGearWhineAnalysis]':
        '''List[OilSealGearWhineAnalysis]: 'ComponentGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentGearWhineAnalysisLoadCases, constructor.new(_5413.OilSealGearWhineAnalysis))
        return value
