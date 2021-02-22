'''_6093.py

DatumCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2122
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5963
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6067
from mastapy._internal.python_net import python_net_import

_DATUM_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'DatumCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumCompoundDynamicAnalysis',)


class DatumCompoundDynamicAnalysis(_6067.ComponentCompoundDynamicAnalysis):
    '''DatumCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _DATUM_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2122.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2122.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5963.DatumDynamicAnalysis]':
        '''List[DatumDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5963.DatumDynamicAnalysis))
        return value

    @property
    def component_dynamic_analysis_load_cases(self) -> 'List[_5963.DatumDynamicAnalysis]':
        '''List[DatumDynamicAnalysis]: 'ComponentDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDynamicAnalysisLoadCases, constructor.new(_5963.DatumDynamicAnalysis))
        return value
