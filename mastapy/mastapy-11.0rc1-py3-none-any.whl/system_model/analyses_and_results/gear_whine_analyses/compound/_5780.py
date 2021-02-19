'''_5780.py

DatumCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2050
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5365
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5758
from mastapy._internal.python_net import python_net_import

_DATUM_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'DatumCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumCompoundGearWhineAnalysis',)


class DatumCompoundGearWhineAnalysis(_5758.ComponentCompoundGearWhineAnalysis):
    '''DatumCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _DATUM_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2050.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2050.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5365.DatumGearWhineAnalysis]':
        '''List[DatumGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5365.DatumGearWhineAnalysis))
        return value

    @property
    def component_gear_whine_analysis_load_cases(self) -> 'List[_5365.DatumGearWhineAnalysis]':
        '''List[DatumGearWhineAnalysis]: 'ComponentGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentGearWhineAnalysisLoadCases, constructor.new(_5365.DatumGearWhineAnalysis))
        return value
